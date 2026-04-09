<?php
sleep(1);
$log_path = __DIR__ . '/intruder_alerts.log';
$current_file = $_GET['file'] ?? '';

// Standardize IP for local consistency
$real_ip = $_SERVER['REMOTE_ADDR'];
if ($real_ip === '::1' || $real_ip === 'localhost') { 
    $real_ip = '127.0.0.1'; 
}

// HARDCODED IDENTITY: MElBcnM0YzZRQUFBRVJsV0Vs
$hwid = "MElBcnM0YzZRQUFBRVJsV0Vs"; 
$id_marker = "ID: " . $hwid;
$hwid_query = "&hwid=" . urlencode($hwid);

// --- STEP 1: THE SENTINEL (BANNING) ---
$depth = substr_count($current_file, '../');
if ($depth > 12) {
    file_put_contents($log_path, "[".date('Y-m-d H:i:s')."] TRAVERSAL_BAN | IP: $real_ip | $id_marker | Path: $current_file\n", FILE_APPEND);
    header("HTTP/1.1 404 Not Found");
    echo "<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL was not found on this server.</p><hr><address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1 Port 8080</address></body></html>";
    exit;
}

// --- STEP 2: THE AUTH TRAP (UNAUTHORIZED ACCESS SCREEN) ---
// This triggers when the hacker tries to access /root or /admin
if (strpos($current_file, 'root') !== false || strpos($current_file, 'admin') !== false) {
    if (!isset($_SERVER['PHP_AUTH_USER'])) {
        header('WWW-Authenticate: Basic realm="Restricted System Administration"');
        header('HTTP/1.0 401 Unauthorized');
        file_put_contents($log_path, "[".date('Y-m-d H:i:s')."] AUTH_CHALLENGE | IP: $real_ip | $id_marker\n", FILE_APPEND);
        echo "<html><head><title>401 Unauthorized</title></head><body><h1>401 Unauthorized</h1><p>This server could not verify that you are authorized to access the document requested.</p><hr><address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1 Port 8080</address></body></html>";
        exit;
    } else {
        $user = $_SERVER['PHP_AUTH_USER'];
        $pass = $_SERVER['PHP_AUTH_PW'];
        file_put_contents($log_path, "[".date('Y-m-d H:i:s')."] CREDENTIALS_STOLEN | IP: $real_ip | $id_marker | User: $user | Pass: $pass\n", FILE_APPEND);
        header('WWW-Authenticate: Basic realm="Restricted System Administration"');
        header('HTTP/1.0 401 Unauthorized');
        exit;
    }
}

// --- STEP 3: ACCESS DENIED SCREEN (403 Forbidden) ---
if ($depth > 0 && $depth < 3) {
    file_put_contents($log_path, "[".date('Y-m-d H:i:s')."] ACCESS_DENIED | IP: $real_ip | $id_marker\n", FILE_APPEND);
    header("HTTP/1.1 403 Forbidden");
    echo "<html><head><title>403 Forbidden</title></head><body><h1>403 Forbidden</h1><p>You don't have permission to access this resource.</p><hr><address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1 Port 8080</address></body></html>";
    exit;
}

// --- STEP 4: DATA POISONING ---
if (isset($_GET['download'])) {
    $filename = $_GET['download'];
    file_put_contents($log_path, "[".date('Y-m-d H:i:s')."] POISON_SENT | IP: $real_ip | $id_marker | File: $filename\n", FILE_APPEND);
    header("Content-Type: text/plain");
    header("Content-Disposition: attachment; filename=\"$filename\"");
    echo "--- MCD INTERNAL ENCRYPTED DATA ---\n";
    for ($i=0; $i<500; $i++) echo "user".rand(10,99).":$6$".bin2hex(random_bytes(8))."\n";
    exit;
}

// --- STEP 5: THE INFINITE MIRROR LOOP ---
$linux_dirs = ['etc', 'var', 'root', 'home', 'bin', 'usr', 'lib', 'boot', 'opt', 'dev'];
$next = $linux_dirs[array_rand($linux_dirs)];
$next_path = $current_file . "../" . $next . "/";

echo "<html><head><title>Index of /system/volumes/internal/</title></head><body style='font-family:sans-serif;'>";
echo "<h1>Index of /system/volumes/internal/</h1><hr><pre>";
echo " <a href='?file=".urlencode($next_path).$hwid_query."'>../</a>\n";
echo " <a href='?file=".urlencode($next_path).$hwid_query."'>$next/</a>                      21-Feb-2026 11:00    -\n";
echo " <a href='?file=".urlencode($current_file)."&download=etc_shadow.bak".$hwid_query."'>etc_shadow.bak</a>             21-Feb-2026 10:45    12.4M\n";
echo " <a href='?file=".urlencode($current_file)."&download=db_backup.sql".$hwid_query."'>db_backup.sql</a>              21-Feb-2026 09:12    45.2M\n";
echo "</pre><hr><address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1 Port 8080</address></body></html>";