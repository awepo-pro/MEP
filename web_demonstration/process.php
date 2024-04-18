<?php
$input = $_POST['input'] ?? '';  // Use the null coalescing operator to check for input
$output = '';
$word_count = 0;

$input_file_path = "input.txt";
if (!empty($input)) {
    if (is_writable($input_file_path)) {
        $input_file = fopen($input_file_path, "w");
        fwrite($input_file, $input);
        fclose($input_file);

        // Trigger NLP processing using shell_exec
        // shell_exec('"C:/Users/ACER/mambaforge/envs/CISC3025_NLP/python.exe" "C:\\Users\\ACER\\Documents\\Code\\MEP\\CISC3025 project 3\\src\\main.py" -a');
        shell_exec('make run');

        // Load the processed tokens from output.json
        $tokensWithLabels = json_decode(file_get_contents('output.json'));

        $inputText = file_get_contents('input.txt'); // Load the input text again for display purposes
        $output = '';
        $lastPosition = 0;
        $word_count = 0;
        $consective_word = false;

        foreach ($tokensWithLabels as $tokenWithLabel) {
            $position = strpos($inputText, $tokenWithLabel->word, $lastPosition);
            $word_count += 1;

            if ($position === false) {
                continue;  // Skip if the token can't be found
            }

            // Append the text from the last position to the start of the current token
            $output .= htmlspecialchars(substr($inputText, $lastPosition, $position - $lastPosition));

            // Highlight "PERSON" tokens
            // if encounter 'Mr., Miss, Dr........' then highlight the next word as well
            if ($consective_word) {
                $output .= htmlspecialchars($tokenWithLabel->word) . '</span>';
                $consective_word = $consective_word ? false : true;
            } else if (
                $tokenWithLabel->word == "Dr." || $tokenWithLabel->word == "Mr." || $tokenWithLabel->word == "Mr"
                || $tokenWithLabel->word == "Mrs." || $tokenWithLabel->word == "Ms." || $tokenWithLabel->word == "Ms"
                || $tokenWithLabel->word == "Mrs" || $tokenWithLabel->word == "Miss"
            ) {
                $output .= '<span class="highlighted">' . htmlspecialchars($tokenWithLabel->word);
                $consective_word = true;
            } else if ($tokenWithLabel->label == "PERSON") {
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
        $output = str_replace('</span> <span class="highlighted">', ' ', $output);

    } else {
        echo "<h1 class=\"error\">Cannot write to file. Check if the file exists and if PHP has write permissions.</h1>";
        return; // Stop further processing in case of error
    }
} else {
    $output = "No input provided.";
}

$response = json_encode(array("result1" => $output, "result2" => $word_count));
echo $response;