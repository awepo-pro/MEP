<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">

    <title>NLP</title>
</head>

<body>

    <?php
    $input = '';
    if (isset($_POST['input'])) {
        $input = $_POST["input"];

        $input_file_path = "input.txt";
        if (is_writable($input_file_path)) {
            $input_file = fopen($input_file_path, "w");
            fwrite($input_file, $input);
            fclose($input_file);
        } else {
            echo "<h1 class=\"error\">Cannot write to file. Check if the file exists and if PHP has write permissions.</h1>";
        }
    }
    ?>

    <header>
        <h1>NLP</h1>
        <div>
            <h3>Name Entity</h3>
            <h3>Recognition</h3>
        </div>
    </header>

    <div class="container">
        <form method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']) ?>">
            <textarea id="input" name="input" rows="28" cols="80"
                placeholder="simplicity is the ultimate sophistication......"><?php echo $input ?></textarea>

            <br><br>

            <button class="btn" value="submit">GO!</button>
        </form>
    </div>

    <?php require_once ('display.php'); ?>

    <div class="container">

        <h1 id="title2">Object and Person</h1>
        <div class="output">
            <p><?php echo $output ?></p>
        </div>
    </div>
</body>

</html>