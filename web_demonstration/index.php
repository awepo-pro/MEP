<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- <link rel="stylesheet" href="background.css"> -->
    <link rel="stylesheet" href="style.css">
    <title>NLP</title>
</head>

<body>

    <?php
    $input = "";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $input = $_POST["input"];
    }

    $input_file = fopen("../CISC3025 project 3/data/input.txt", "w");
    $history_file = fopen("../CISC3025 project 3/data/history.txt", "a");

    fwrite($input_file, $input);
    fwrite($history_file, $input);
    fwrite($history_file, "\n\n******************************************************\n\n");

    fclose($input_file);
    fclose($history_file);
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
                placeholder="simplicity is the ultimate sophistication......"><?php echo $input ?></textarea><br><br>

            <button class="btn"><a href="#title2">GO!</a></button>
        </form>
    </div>

    <?php
    /*
        get result from python script, 
    */

    // suppose get_ind and get_token is returned by python
    $get_ind = [2];
    $get_token = ['I', 'am', 'Anton'];

    $cnt = 0;
    $output = '';

    // for each word, if the token is name, highlight it
    for ($i = 0; $i < count($get_token); $i++) {
        if ($cnt < count($get_ind) && $i == $get_ind[$cnt]) {
            $output .= '<span class="highlighted">' . $get_token[$i] . '</span> ';
            $cnt++;
        } else {
            $output .= $get_token[$i] . ' ';
        }
    }

    // echo $output;
    ?>

    <div class="container">

        <h1 id="title2">Object and Person</h1>
        <div class="output">
            <p><?php echo $output ?></p>
        </div>
    </div>

    <!-- <script>

        var scrollButton = document.querySelector('.btn');
        console.log(scrollButton);

        scrollButton.addEventListener('click', function () {
            console.log('hello');
            window.scrollTo({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        });

    </script> -->
</body>

</html>