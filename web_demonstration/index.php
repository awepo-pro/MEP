<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NLP</title>
</head>

<body>

    <?php
    $input = "";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $input = $_POST["input"];
    }

    $input_file = fopen("../CISC3025 project 3/data/input.txt", "w") or die("Unable to open file!");
    fwrite($input_file, $input);
    fclose($input_file);
    ?>

    <h1>NLP</h1>

    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <label for="text">Enter text:</label><br>
        <textarea id="input" name="input" rows="40" cols="100"><?php echo $input ?></textarea><br><br>

        <input type="submit" value="Submit">
        <input type="reset" value="Reset">
    </form>

    <h1>Output</h1>

    <?php
    echo $input;
    ?>

</body>

</html>