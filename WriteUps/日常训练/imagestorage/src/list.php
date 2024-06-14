<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Image Storage</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    </head>
    <body>
        <?php if(!isset($_SESSION["username"])) echo "<script>alert('login first.')</script><meta http-equiv=\"refresh\" content=\"0;url=/login.php\" />"; ?>
        <nav class="navbar navbar-expand-lg" style="background-color: #e3f2fd;">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">Image Storage</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/list.php">Storage</a>
                        </li>
                    </ul>
                </div>
                <?php echo "Welcome ".$_SESSION['username']."!!"; ?>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/logout.php">Logout</a>
                    </li>
                </ul>
            </div>
        </nav>
        <table class="table" style="margin-top: 50px">
            <thead>
                <tr>
                    <th scope="col">id</th>
                    <th scope="col">Filename</th>
                </tr>
            </thead>
            <tbody>
            <?php   
            $dir = "./images/";
            $id = 1;
            if (is_dir($dir)){                              
                if ($dh = opendir($dir)){                     
                    while (($file = readdir($dh)) !== false){
                        if($file != "." && $file != ".."){
                            echo "<tr><th scope=\"row\">".strval($id)."</th><td><a href=\"/view.php?filename=".$file."\">".$file."</td></tr>";
                            $id++;
                        }
                    }                                           
                    closedir($dh);                              
                }                                             
            }           
            ?>
            </tbody>
        </table>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.min.js" integrity="sha384-mQ93GR66B00ZXjt0YO5KlohRA5SY2XofN4zfuZxLkoj1gXtW8ANNCe9d5Y3eG5eD" crossorigin="anonymous"></script>
    </body>
</html>