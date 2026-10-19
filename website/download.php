<?php
$isoDir = __DIR__ . '/iso';
$countFile = __DIR__ . '/downloads.count';

function readCount($file) {
    return is_file($file) ? (int) trim(file_get_contents($file)) : 0;
}

if (($_GET['action'] ?? '') === 'count') {
    header('Content-Type: application/json');
    header('Cache-Control: no-store');
    echo json_encode(['value' => readCount($countFile)]);
    exit;
}

$sums = @file_get_contents($isoDir . '/latest.sha256');
$parts = $sums ? preg_split('/\s+/', trim($sums)) : [];
$name = isset($parts[1]) ? ltrim($parts[1], '*') : '';

if (!preg_match('/^niixaos-[\w.-]+\.iso$/', $name) || !is_file("$isoDir/$name")) {
    http_response_code(404);
    header('Content-Type: text/plain');
    echo "No ISO is available right now. Please try again later.";
    exit;
}

$agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
$range = $_SERVER['HTTP_RANGE'] ?? '';
$isBot = $agent === '' || preg_match('/bot|crawl|spider|slurp|preview|facebookexternalhit/i', $agent);
$isResume = $range !== '' && !preg_match('/^bytes=0-/', $range);

if ($_SERVER['REQUEST_METHOD'] === 'GET' && !$isBot && !$isResume) {
    $fp = fopen($countFile, 'c+');
    if ($fp && flock($fp, LOCK_EX)) {
        $count = (int) trim(stream_get_contents($fp));
        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, (string) ($count + 1));
        fflush($fp);
        flock($fp, LOCK_UN);
    }
    if ($fp) fclose($fp);
}

header('Cache-Control: no-store');
header('Location: iso/' . rawurlencode($name), true, 302);
