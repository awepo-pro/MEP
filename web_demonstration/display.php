<?php

$inputText = file_get_contents('input.txt');

if (!empty($input)) {
    shell_exec('"C:/Users/ACER/mambaforge/envs/CISC3025_NLP/python.exe" "C:\Users\ACER\Documents\Code\MEP\CISC3025 project 3\src\main.py" -a');
}

$tokensWithLabels = json_decode(file_get_contents('output.json')); // accsociative array

$output = '';
$lastPosition = 0;

foreach ($tokensWithLabels as $tokenWithLabel) {
    // Find the position of the current token in the input text starting from the last matched position
    $position = strpos($inputText, $tokenWithLabel->word, $lastPosition);

    // Append the text from the last position to the start of the current token (this includes spaces, punctuation, and newlines)
    $output .= htmlspecialchars(substr($inputText, $lastPosition, $position - $lastPosition));

    // Check if the current token should be highlighted
    if ($tokenWithLabel->label === "PERSON") {
        $output .= '<span class="highlighted">' . htmlspecialchars($tokenWithLabel->word) . '</span>';
    } else {
        $output .= htmlspecialchars($tokenWithLabel->word);
    }

    // Update the last position to the end of the current token
    $lastPosition = $position + strlen($tokenWithLabel->word);
}

// Append any remaining text after the last token
$output .= htmlspecialchars(substr($inputText, $lastPosition));
$output = nl2br($output);

// echo $output;
?>