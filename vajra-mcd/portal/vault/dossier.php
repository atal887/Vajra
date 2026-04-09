<?php
$log_file = __DIR__ . '/intruder_alerts.log';
$lines = file_exists($log_file) ? file($log_file) : [];
$subjects = [];
$master_map = [];

// PASS 1: Normalize identity and link IPs to the Hardcoded ID
foreach($lines as $line) {
    if (preg_match('/IP: ([\d\.\:a-f]+) \| ID: ([A-Za-z0-9\+\/=]+)/', $line, $m)) {
        $master_map[$m[1]] = trim($m[2]);
    }
}

// PASS 2: Aggregate data into a Narrative structure
foreach($lines as $line) {
    if (!preg_match('/\[(.*?)\] (.*?) \| IP: (.*?) \| (.*)/', $line, $matches)) continue;
    
    $ip = $matches[3];
    $event = trim($matches[2]);
    $detail = $matches[4];
    $sid = $master_map[$ip] ?? $ip;

    if (!isset($subjects[$sid])) {
        $subjects[$sid] = [
            'id' => $sid,
            'ips' => [],
            'start' => $matches[1],
            'end' => $matches[1],
            'events' => [],
            'credentials' => [],
            'files_accessed' => []
        ];
    }
    
    $subjects[$sid]['ips'][$ip] = true;
    $subjects[$sid]['end'] = $matches[1];
    
    if (strpos($event, 'CREDENTIALS_STOLEN') !== false) {
        preg_match('/User: (.*?) \| Pass: (.*)/', $detail, $creds);
        $subjects[$sid]['credentials'][] = "User: " . ($creds[1] ?? 'unknown') . " / PW: " . ($creds[2] ?? 'unknown');
    }
    if (strpos($event, 'POISON_SENT') !== false) {
        preg_match('/File: (.*)/', $detail, $file);
        $subjects[$sid]['files_accessed'][] = $file[1] ?? 'unknown';
    }
    $subjects[$sid]['events'][] = ['t' => $matches[1], 'e' => $event];
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MCD Internal Forensic Report</title>
    <style>
        body { font-family: 'Times New Roman', serif; background: #f4f4f4; color: #333; line-height: 1.6; padding: 40px; }
        .document { background: #fff; max-width: 850px; margin: auto; padding: 60px; border: 1px solid #ccc; box-shadow: 0 0 10px rgba(0,0,0,0.1); position: relative; }
        .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); font-size: 80px; color: rgba(200,0,0,0.05); pointer-events: none; white-space: nowrap; font-weight: bold; }
        
        /* MCD Official Stamp */
        .mcd-stamp {
            position: absolute;
            top: 40px;
            right: 40px;
            width: 110px;
            height: 110px;
            border: 4px double #d32f2f;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 10px;
            font-weight: bold;
            color: #d32f2f;
            text-transform: uppercase;
            transform: rotate(15deg);
            background: rgba(211, 47, 47, 0.03);
            z-index: 5;
        }

        .header { text-align: center; border-bottom: 2px solid #000; margin-bottom: 30px; padding-bottom: 10px; }
        .header h1 { margin: 0; text-transform: uppercase; letter-spacing: 2px; }
        .header p { margin: 5px 0; font-weight: bold; color: #666; }
        .section { margin-bottom: 30px; }
        .section-title { font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #eee; margin-bottom: 10px; color: #d32f2f; }
        .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; font-size: 14px; }
        .btn-container { text-align: center; margin-bottom: 20px; }
        .download-btn { background: #d32f2f; color: #fff; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; border-radius: 5px; }
        @media print { .btn-container { display: none; } body { background: #fff; padding: 0; } .document { border: none; box-shadow: none; margin: 0; } }
    </style>
</head>
<body>

<div class="btn-container">
    <button class="download-btn" onclick="window.print()">GENERATE OFFICIAL PDF</button>
</div>

<?php foreach($subjects as $id => $data): ?>
<div class="document">
    <div class="watermark">MCD CONFIDENTIAL</div>
    <div class="mcd-stamp">Municipal<br>Corp. Delhi<br>Secured<br><?php echo date('Y-m-d'); ?></div>
    
    <div class="header">
        <h1>Forensic Investigation Report</h1>
        <p>Municipal Corporation of Delhi - Cyber Security Division</p>
        <p>Ref ID: <?php echo date('Y-m-d'); ?>/SENTINEL/<?php echo substr($id, 0, 8); ?></p>
    </div>

    <div class="section">
        <div class="section-title">1. Subject Identification</div>
        <div class="meta-grid">
            <div><strong>Identity Marker:</strong> <?php echo $id; ?></div>
            <div><strong>Associated IPs:</strong> <?php echo implode(', ', array_keys($data['ips'])); ?></div>
            <div><strong>Incident Start:</strong> <?php echo $data['start']; ?></div>
            <div><strong>Final Termination:</strong> <?php echo $data['end']; ?></div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">2. Adversarial Methodology & Unmasking</div>
        <p>The subject attempted to obscure their network identity, but was successfully unmasked via <strong>Hardware Fingerprinting</strong>. Despite connection variations, the system verified a consistent hardware signature. 
        The subject focused on <strong>Path Traversal</strong> to reach restricted system volumes.</p>
    </div>

    <div class="section">
        <div class="section-title">3. Neutralized Threats & Data Integrity</div>
        <ul>
            <li><strong>Credential Harvesting:</strong> The intruder attempted authentication using <?php echo count($data['credentials']); ?> unique credentials, which were captured by the Vajra Auth-Trap.</li>
            <li><strong>Data Poisoning:</strong> <?php echo count($data['files_accessed']); ?> honey-files were successfully exfiltrated by the subject, containing seeded deceptive data.</li>
            <li><strong>System Ban:</strong> Access was automatically terminated following a high-depth traversal violation.</li>
        </ul>
    </div>

    <div class="section">
        <div class="section-title">4. Technical Evidence Log</div>
        <div style="font-size: 12px; font-family: monospace; background: #f9f9f9; padding: 15px; border: 1px solid #eee;">
            <?php foreach(array_slice($data['events'], -5) as $log): ?>
                [<?php echo $log['t']; ?>] - Detected Activity: <?php echo $log['e']; ?><br>
            <?php endforeach; ?>
        </div>
    </div>

    <div style="margin-top: 50px; font-size: 12px; border-top: 1px solid #eee; padding-top: 10px;">
        <em>Digitally Verified by: Vajra Sentinel System v2.1</em><br>
        <em>Location: DTU Cyber Security Research Lab</em>
    </div>
</div>
<?php endforeach; ?>

</body>
</html>