<?php
$input = $_POST['input'] ?? '';  // Use the null coalescing operator to check for input

$input_file_path = "input.txt";
if (!empty($input)) {
    if (is_writable($input_file_path)) {
        $input_file = fopen($input_file_path, "w");
        fwrite($input_file, $input);
        fclose($input_file);

        // Trigger NLP processing using shell_exec
        shell_exec('make run');

        // Load the processed tokens from output.json
        $tokensWithLabels = json_decode(file_get_contents('output.json'));

        $inputText = file_get_contents('input.txt'); // Load the input text again for display purposes
        $output = '';
        $lastPosition = 0;

        foreach ($tokensWithLabels as $tokenWithLabel) {
            $position = strpos($inputText, $tokenWithLabel->word, $lastPosition);

            if ($position === false) {
                continue;  // Skip if the token can't be found
            }

            // Append the text from the last position to the start of the current token
            $output .= htmlspecialchars(substr($inputText, $lastPosition, $position - $lastPosition));

            // Highlight "PERSON" tokens
            if ($tokenWithLabel->label === "PERSON") {
                $output .= '<span class="highlighted">' . htmlspecialchars($tokenWithLabel->word) . '</span>';
            } else {
                $output .= htmlspecialchars($tokenWithLabel->word);
            }

            // Update the last position
            $lastPosition = $position + strlen($tokenWithLabel->word);
        }

        // Append any remaining text after the last token
        $output .= htmlspecialchars(substr($inputText, $lastPosition));
        $output = nl2br($output);

    } else {
        echo "<h1 class=\"error\">Cannot write to file. Check if the file exists and if PHP has write permissions.</h1>";
        return; // Stop further processing in case of error
    }
} else {
    $output = "No input provided.";
}

// Output the final processed text
echo $output;
?>
