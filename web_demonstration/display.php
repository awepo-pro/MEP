<?php

if (!empty($input)) {
    shell_exec('make run');
}

$get_from_py = json_decode(file_get_contents('output.json')); // accsociative array

$get_label = [];
$get_token = [];

for ($i = 0; $i < count($get_from_py); $i++) {
    $tmp_array = (array) $get_from_py[$i];
    array_push($get_label, $tmp_array['label']);
    array_push($get_token, $tmp_array['word']);
}

$output = '';

// for each word, if the token is name, highlight it
for ($i = 0; $i < count($get_token); $i++) {
    if ($get_label[$i] == "PERSON") {
        $output .= '<span class="highlighted">' . $get_token[$i] . '</span> ';
    } else {
        $output .= $get_token[$i] . ' ';
    }
}

// echo $output;
?>