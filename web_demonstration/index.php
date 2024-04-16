<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">

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

    <?php $output = $output ?? ''; $input = $input ?? ''?>

        <div class="container">
            <div class="flex-child">
                <form id="nlpForm" method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']) ?>">
                    <textarea id="input" name="input" rows="1" cols="80"
                        placeholder="simplicity is the ultimate sophistication......"><?php echo $input ?></textarea>
                </form>
            </div>

            <div class="flex-child">
                <h1 id="title2">Object and Person</h1>
                <div class="output">
                    <p id="output"><?php echo $output ?></p>
                </div>
            </div>
        </div>

    <script src="script.js"></script>
    <script>
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
    </script>
</body>
</html>