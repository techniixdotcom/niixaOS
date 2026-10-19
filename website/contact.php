<?php
$to = 'your email';
$from = 'niixaOS website <your email>';
$minSeconds = 2;
$maxPerHour = 5;

$smtpHost = '';
$smtpPort = 465;
$smtpSecure = 'ssl';
$smtpUser = '';
$smtpPass = '';

if (is_file(__DIR__ . '/contact-config.php')) {
    include __DIR__ . '/contact-config.php';
}

ini_set('display_errors', '0');
header('Content-Type: application/json');
header('Cache-Control: no-store');

register_shutdown_function(function () {
    $e = error_get_last();
    if ($e && in_array($e['type'], array(E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR))) {
        if (!headers_sent()) {
            http_response_code(200);
            header('Content-Type: application/json');
        }
        echo json_encode(array('ok' => false, 'error' => 'server error: ' . $e['message'] . ' (line ' . $e['line'] . ')'));
    }
});

function reply($ok, $error = null) {
    echo json_encode($ok ? array('ok' => true) : array('ok' => false, 'error' => $error));
    exit;
}

function cut($value, $max) {
    $value = (string) $value;
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max, 'UTF-8');
    }
    return substr($value, 0, $max);
}

function oneLine($value, $max) {
    return trim(cut(str_replace(array("\r", "\n"), ' ', $value), $max));
}

function newToken() {
    if (function_exists('random_bytes')) {
        return bin2hex(random_bytes(16));
    }
    if (function_exists('openssl_random_pseudo_bytes')) {
        return bin2hex(openssl_random_pseudo_bytes(16));
    }
    return sha1(uniqid('', true) . mt_rand());
}

function sameToken($a, $b) {
    if (function_exists('hash_equals')) {
        return hash_equals($a, $b);
    }
    return $a === $b;
}

function address($value) {
    return preg_match('/<([^>]+)>/', $value, $m) ? $m[1] : trim($value);
}

function smtpRead($fp) {
    $data = '';
    while (($line = fgets($fp, 1024)) !== false) {
        $data .= $line;
        if (strlen($line) < 4 || $line[3] === ' ') break;
    }
    return $data;
}

function smtpCmd($fp, $cmd, $expect, $show = null) {
    if ($cmd !== null) fwrite($fp, $cmd . "\r\n");
    $res = smtpRead($fp);
    if ((int) substr($res, 0, 3) !== $expect) {
        throw new Exception('mail server said "' . trim($res) . '" to ' . ($show !== null ? $show : strtok((string) $cmd, ' ')));
    }
    return $res;
}

function smtpSend($host, $port, $secure, $user, $pass, $from, $to, $replyTo, $subject, $body) {
    $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $fp = @stream_socket_client($remote, $errno, $errstr, 15);
    if (!$fp) {
        throw new Exception("could not connect to $host:$port ($errstr)");
    }
    stream_set_timeout($fp, 15);
    $me = isset($_SERVER['SERVER_NAME']) ? $_SERVER['SERVER_NAME'] : 'localhost';

    smtpCmd($fp, null, 220, 'connect');
    smtpCmd($fp, "EHLO $me", 250);
    if ($secure === 'tls') {
        smtpCmd($fp, 'STARTTLS', 220);
        if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
            throw new Exception('could not start TLS with the mail server');
        }
        smtpCmd($fp, "EHLO $me", 250);
    }
    if ($user !== '') {
        smtpCmd($fp, 'AUTH LOGIN', 334);
        smtpCmd($fp, base64_encode($user), 334, 'the username');
        smtpCmd($fp, base64_encode($pass), 235, 'the password');
    }
    smtpCmd($fp, 'MAIL FROM:<' . address($from) . '>', 250);
    smtpCmd($fp, 'RCPT TO:<' . address($to) . '>', 250);
    smtpCmd($fp, 'DATA', 354);

    $headers = array(
        'Date: ' . date('r'),
        'From: ' . $from,
        'To: ' . $to,
        'Reply-To: ' . $replyTo,
        'Subject: ' . $subject,
        'Message-ID: <' . sha1(uniqid('', true)) . '@' . substr(strrchr(address($from), '@'), 1) . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    );
    $text = str_replace(array("\r\n", "\r"), "\n", $body);
    $text = preg_replace('/^\./m', '..', $text);
    $data = implode("\r\n", $headers) . "\r\n\r\n" . str_replace("\n", "\r\n", $text) . "\r\n.";
    smtpCmd($fp, $data, 250, 'the message');
    fwrite($fp, "QUIT\r\n");
    fclose($fp);
}

@session_start();

$action = isset($_GET['action']) ? $_GET['action'] : '';

if ($action === 'token') {
    $_SESSION['contact_token'] = newToken();
    $_SESSION['contact_time'] = time();
    echo json_encode(array('token' => $_SESSION['contact_token']));
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    reply(false, 'method not allowed');
}

if (!empty($_POST['website'])) {
    reply(true);
}

$token = isset($_POST['token']) ? (string) $_POST['token'] : '';
$saved = isset($_SESSION['contact_token']) ? $_SESSION['contact_token'] : '';
if ($saved === '' || !sameToken($saved, $token)) {
    reply(false, 'the form expired, reload the page and try again');
}

$since = isset($_SESSION['contact_time']) ? $_SESSION['contact_time'] : 0;
if (time() - $since < $minSeconds) {
    reply(false, 'please wait a moment before sending');
}

$sent = array();
if (isset($_SESSION['contact_sent']) && is_array($_SESSION['contact_sent'])) {
    foreach ($_SESSION['contact_sent'] as $t) {
        if ($t > time() - 3600) $sent[] = $t;
    }
}
if (count($sent) >= $maxPerHour) {
    reply(false, 'too many messages, please try again later');
}

$name = oneLine(isset($_POST['name']) ? $_POST['name'] : '', 100);
$email = oneLine(isset($_POST['email']) ? $_POST['email'] : '', 200);
$subject = oneLine(isset($_POST['subject']) ? $_POST['subject'] : '', 200);
$msg = trim(cut(isset($_POST['msg']) ? $_POST['msg'] : '', 5000));

if ($name === '' || $email === '' || $subject === '' || $msg === '') {
    reply(false, 'please fill in all fields');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    reply(false, 'please enter a valid email address');
}

$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '?';
$body = "Name: $name\nEmail: $email\nIP: $ip\n\n$msg\n";
if ($smtpHost === '' && !function_exists('mail')) {
    reply(false, 'sending mail is turned off on this server - fill in the SMTP settings in contact-config.php');
}

$encoded = '=?UTF-8?B?' . base64_encode('[niixaOS] ' . $subject) . '?=';

if ($smtpHost !== '') {
    $tries = array(array($smtpPort, $smtpSecure), array(465, 'ssl'), array(587, 'tls'), array(475, 'ssl'));
    $done = array();
    $error = '';
    foreach ($tries as $try) {
        $key = $try[0] . $try[1];
        if (isset($done[$key])) continue;
        $done[$key] = true;
        try {
            smtpSend($smtpHost, $try[0], $try[1], $smtpUser, $smtpPass, $from, $to, $email, $encoded, $body);
            $error = '';
            break;
        } catch (Exception $e) {
            $error = $e->getMessage();
            if (strpos($error, 'could not connect') !== 0 && strpos($error, 'TLS') === false) break;
        }
    }
    if ($error !== '') {
        reply(false, $error);
    }
} else {
    $headers = implode("\r\n", array(
        'From: ' . $from,
        'Reply-To: ' . $email,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
    ));
    if (!@mail($to, $encoded, $body, $headers)) {
        reply(false, 'the mail server did not accept the message');
    }
}

$sent[] = time();
$_SESSION['contact_sent'] = $sent;
unset($_SESSION['contact_token']);
reply(true);
