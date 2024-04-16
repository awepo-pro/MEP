<!-- declare $input variable -->
<?php $input = ''; ?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">

    <!-- google font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Imbue:opsz,wght@10..100,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Sedan:ital@0;1&display=swap"
        rel="stylesheet">
    <title>NLP</title>
</head>

<body>
    <header>
        <h1>NLP</h1>
        <div>
            <h3>Named Entity</h3>
            <h3>Recognition</h3>
        </div>
    </header>

    <div class="container">
        <div class="flex-child">
            <form id="nlpForm" method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']) ?>">
                <textarea id="input" name="input" rows="19.5" cols="80"
                    placeholder="simplicity is the ultimate sophistication......"><?php echo $input ?></textarea>
            </form>
        </div>

        <!-- empty space -->
        <div></div>

        <div class="flex-child">
            <!-- <h1 id="title2">Object and Person</h1> -->
            <div class="output">
                <p id="output"><?php echo $output ?></p>
            </div>
            <div class="wc">word: <span id="wordCount"></span></div>
        </div>
    </div>

    <script src="script.js"></script>
    <!-- <script>
        const textarea = document.getElementById('input');

        function autoResize() {
            // Reset the height to shrink if text is deleted
            textarea.style.height = 'auto';
            // Set the height based on the scroll height of the textarea
            textarea.style.height = textarea.scrollHeight + 'px';
        }

        // Event listener for input event
        textarea.addEventListener('input', autoResize);
        autoResize();
    </script> -->
</body>

</html>