$ErrorActionPreference = 'Stop'
$workspace = 'C:\Users\colt3\OpenBot\Agents\agent-e5512a52-ac06-4a63-94f2-08e6d027ff75'
$sourceRoot = 'C:\Users\colt3\OpenBot\Shared\Transfers\c485f49c-1d68-41b7-87cf-edc619829f18'
$outputRoot = 'C:\Users\colt3\OpenBot\Shared\SOW-2026-11-03'
$ffmpeg = Join-Path $workspace '.tools\transcription\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe'
$whisper = Join-Path $workspace '.tools\transcription\whisper\Release\whisper-cli.exe'
$model = Join-Path $workspace '.tools\transcription\ggml-small.en.bin'
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
$statusPath = Join-Path $outputRoot 'transcription-status.json'
$manifest = Get-Content -LiteralPath (Join-Path $sourceRoot '.openbot-transfer.json') -Raw | ConvertFrom-Json
$records = @()
$byHash = @{}
try {
    $index = 0
    foreach ($attachment in $manifest.attachments) {
        $index++
        $sourcePath = Join-Path $sourceRoot $attachment.relativePath
        $hash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($hash -ne $attachment.sha256) { throw "Source hash mismatch: $($attachment.name)" }
        $record = [ordered]@{ source_id = ('source-{0:d2}' -f $index); filename = $attachment.name; sha256 = $hash; original_path = $sourcePath; duplicate_of = $null; transcript_srt = $null }
        if ($byHash.ContainsKey($hash)) {
            $record.duplicate_of = $byHash[$hash].source_id
            $record.transcript_srt = $byHash[$hash].transcript_srt
        } else {
            @{ status = 'running'; current_source = $attachment.name; completed_sources = $records.Count; total_sources = $manifest.attachments.Count; updated_at = (Get-Date).ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath $statusPath -Encoding UTF8
            $base = Join-Path $outputRoot $record.source_id
            $wavPath = $base + '.wav'
            $convertLog = $base + '-conversion.log'
            $asrLog = $base + '-asr.log'
            $ErrorActionPreference = 'Continue'
            & $ffmpeg -hide_banner -loglevel error -y -i $sourcePath -vn -ar 16000 -ac 1 -c:a pcm_s16le $wavPath 2>&1 | Out-File -LiteralPath $convertLog -Encoding UTF8
            $ErrorActionPreference = 'Stop'
            if ($LASTEXITCODE -ne 0) { throw "Audio conversion failed: $($attachment.name)" }
            $ErrorActionPreference = 'Continue'
            & $whisper -m $model -f $wavPath -t 6 -otxt -osrt -oj -of $base 2>&1 | Out-File -LiteralPath $asrLog -Encoding UTF8
            $ErrorActionPreference = 'Stop'
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath ($base + '.srt'))) { throw "Transcription failed: $($attachment.name)" }
            $record.transcript_srt = $base + '.srt'
            $byHash[$hash] = $record
        }
        $records += [pscustomobject]$record
        $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputRoot 'source-inventory.json') -Encoding UTF8
    }
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add('# Source recording transcripts - 3 November 2026')
    $lines.Add('')
    $lines.Add('Machine-generated transcription using whisper.cpp small.en, not human-verified. Treat uncertain words, names, measurements and quantities as unresolved; do not silently correct or invent them. The original ten media files remain the primary evidence. Botkin sample documents supply formatting and branding only, never job facts. Do not infer a property address from samples.')
    $lines.Add('')
    $lines.Add('All ten source files are inventoried below. Exact byte-identical copies share one transcript and must not duplicate work or quantities. Hashes were recomputed and matched the original transfer manifest.')
    foreach ($record in $records) {
        $lines.Add('')
        $lines.Add(('## {0}: {1}' -f $record.source_id, $record.filename))
        $lines.Add(('SHA256: {0}' -f $record.sha256))
        if ($record.duplicate_of) {
            $lines.Add(('Exact byte-identical duplicate of {0}; see that source transcript. This is still one of the ten uploaded attachments.' -f $record.duplicate_of))
        } else {
            $lines.Add('Elapsed timestamps restart at 00:00 for each original recording:')
            $lines.Add('```srt')
            $lines.Add((Get-Content -LiteralPath $record.transcript_srt -Raw))
            $lines.Add('```')
        }
    }
    $lines | Set-Content -LiteralPath (Join-Path $outputRoot 'recording-transcripts.md') -Encoding UTF8
    @{ status = 'complete'; completed_sources = $records.Count; unique_recordings = $byHash.Count; combined_transcript = (Join-Path $outputRoot 'recording-transcripts.md'); updated_at = (Get-Date).ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath $statusPath -Encoding UTF8
} catch {
    @{ status = 'failed'; error = $_.Exception.Message; completed_sources = $records.Count; updated_at = (Get-Date).ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath $statusPath -Encoding UTF8
    throw
}
