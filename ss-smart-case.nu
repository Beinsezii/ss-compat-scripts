#! /usr/bin/env nu
use std assert

def png_from_list [png: string, pngs: list<string>] -> string? {
    if $png in $pngs {
        return null
    } else {
        let ref = ($png | str downcase)
        for p in $pngs {
            if ($p | str downcase) == $ref {
                return $p
            }
        }
    }
    return null
}

def main [] {
    assert not (ls | where name == mod_info.json | is-empty ) "Script must be run from a mod directory!"

    let data_files = (glob "data/**/*")
    let pngs = (glob "graphics/**/*.png" | path relative-to $env.PWD)
    let formats = [
        [extension, type, sprites, guards];
        [ship, json, [spriteName], [hullId]]
        [skin, json, [spriteName], [skinHullId]]
        [wpn, json, [turretSprite, turretGunSprite, hardpointSprite, hardpointGunSprite], []]
        [proj, json, [bulletSprite, sprite, textureType], []],
        [csv, csv, [icon, path, portrait, image, sprite], []],
    ]
    $data_files | par-each { |f|
        mut changelog = ''
        let ext = ($f | path parse | get extension)
        for format in $formats {
            if $format.extension == $ext {
                mut data = []
                try {
                    $data = match $format.type {
                        json => (open $f | from json),
                        csv => (open $f),
                    }
                } catch {break}

                let original = $data

                for sprite in $format.sprites {
                    mut new = ''
                    try {$new = ($data | get $sprite)} catch {continue}
                    let old = $new

                    $new = ($new | str replace -a '\' '/')

                    # handle lists of strings
                    if ($new | describe) != string {
                        $new = ($new | each -k { |i| png_from_list $i $pngs | default $i })
                        assert ( ($new | enumerate | length) == ($old | enumerate | length) )
                    } else {
                        let maybe_png = png_from_list $new $pngs
                        if $maybe_png != null { $new = $maybe_png }
                    }
                    if $new != $old {
                        mut guarded = true
                        for g in $format.guards {
                            try { $guarded = (($data | get $g) in $new)
                            } catch {continue}
                        }
                        if not $guarded { print $"($sprite): ($new) -> ($old) failed guard check" }
                        for vals in ($new | enumerate) {
                            if ($new | describe) != string {
                                $changelog = $"($changelog)\t($sprite): ($old | enumerate | get $vals.index | get item) -> ($vals.item)\n"
                            } else {
                                $changelog = $"($changelog)\t($sprite): ($old) -> ($vals.item)\n"
                            }
                        }
                        $data = ($data | update $sprite $new)
                    }
                }
                if $original != $data {
                    $data | to json | save -f $f
                }
            }
        }
        if not ($changelog | is-empty) {print $"($f):\n($changelog)"}
    }
    null
}
