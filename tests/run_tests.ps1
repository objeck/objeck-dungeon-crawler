# Warden of Greyhold - Regression Test Runner
param([string]$filter = "")

$env:OBJECK_LIB_PATH = "C:\Users\objec\Documents\Code\objeck-lang\core\release\deploy-x64\lib"
$env:PATH = "$env:PATH;C:\Users\objec\Documents\Code\objeck-lang\core\release\deploy-x64\bin;C:\Users\objec\Documents\Code\objeck-lang\core\release\deploy-x64\lib\sdl"

$obc  = "C:\Users\objec\Documents\Code\objeck-lang\core\release\deploy-x64\bin\obc.exe"
$obr  = "C:\Users\objec\Documents\Code\objeck-lang\core\release\deploy-x64\bin\obr.exe"
$td   = "C:\Users\objec\Documents\Code\objeck-dungeon-crawler\tests"
$gd   = "C:\Users\objec\Documents\Code\objeck-dungeon-crawler"

$gs   = @("$gd\dungeon_managers.obs","$gd\dungeon_eninities.obs",
          "$gd\dungeon_monsters.obs","$gd\dungeon_ai.obs","$gd\overworld_manager.obs")
$libs = "cipher,net,gen_collect,sdl2,json,sdl_game,misc,ollama"

$tests = @(
    @{ N="saveload";   Extra=@();    Libs="cipher,net,json,misc"; D="JSON save/load round-trip"      },
    @{ N="worldgen";   Extra=$gs;    Libs=$libs;                  D="WorldGen map validation"         },
    @{ N="overworld";  Extra=$gs;    Libs=$libs;                  D="Overworld passability & events"  },
    @{ N="player";     Extra=$gs;    Libs=$libs;                  D="Player stats & level-up"         },
    @{ N="spells";     Extra=$gs;    Libs=$libs;                  D="Spell system"                    },
    @{ N="items";      Extra=$gs;    Libs=$libs;                  D="Weapon / armor / potions"        },
    @{ N="combat";     Extra=$gs;    Libs=$libs;                  D="Combat math & monster factory"   },
    @{ N="town";       Extra=$gs;    Libs=$libs;                  D="Town economy logic"              },
    @{ N="overworld2"; Extra=$gs;    Libs=$libs;                  D="Overworld Phase 2-4 logic"       }
)

if ($filter) { $tests = $tests | Where-Object { $_.N -like "*$filter*" } }

$W = 56
Write-Host ""
Write-Host ("=" * $W)
Write-Host "  Warden of Greyhold  -  Regression Tests"
Write-Host ("=" * $W)
Write-Host ("{0,-8} {1}" -f "Status","Test")
Write-Host ("-" * $W)

$nPass = 0; $nFail = 0; $nBuild = 0

foreach ($t in $tests) {
    $fname = "test_$($t.N)"
    $obe   = "$td\$fname.obe"
    $srcs  = @("$td\$fname.obs") + $t.Extra
    $srcArg = $srcs -join ","

    # Build
    $bOut = & $obc -src $srcArg -lib $t.Libs -dest $obe 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errLine = ($bOut | Select-String "Expected|Undefined|Invalid" | Select-Object -First 1)
        $errMsg  = if ($errLine) { $errLine.ToString().Trim() -replace "^obc.exe : ","" } else { "compile error" }
        if ($errMsg.Length -gt 44) { $errMsg = $errMsg.Substring(0,41) + "..." }
        Write-Host ("[BUILD] {0,-30} {1}" -f $t.D.PadRight(30), $errMsg) -ForegroundColor Yellow
        $nBuild++
        Remove-Item $obe -EA SilentlyContinue
        continue
    }

    # Run
    $out = & $obr $obe 2>&1
    Remove-Item $obe -EA SilentlyContinue

    $passLine = $out | Where-Object { $_ -match "^PASS:" }
    $failLine = $out | Where-Object { $_ -match "^FAIL:" }
    $detLines = $out | Where-Object { $_ -match "^\s+FAIL:" }

    if ($failLine) {
        $det = ""
        if ($detLines) {
            $det = ($detLines | Select-Object -First 1).ToString().Trim()
            if ($det.Length -gt 44) { $det = $det.Substring(0,41) + "..." }
        }
        Write-Host ("[FAIL] {0,-30} {1}" -f $t.D, $det) -ForegroundColor Red
        $nFail++
    } else {
        Write-Host ("[PASS] {0}" -f $t.D) -ForegroundColor Green
        $nPass++
    }
}

$total = $nPass + $nFail + $nBuild
Write-Host ("-" * $W)
$s = "$nPass/$total passed"
if ($nFail -gt 0)  { $s += "   $nFail failed" }
if ($nBuild -gt 0) { $s += "   $nBuild build errors" }
Write-Host "  $s"
Write-Host ("=" * $W)
Write-Host ""

if ($nFail -gt 0 -or $nBuild -gt 0) { exit 1 }
