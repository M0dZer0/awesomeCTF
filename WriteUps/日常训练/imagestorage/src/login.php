<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Image Storage</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <style>
            * { padding: 0; margin: 0; }
            html, body {
                height: 100%;
                background: #ffffff;
            }
            #container {
                display: flex;
                flex-direction: row;
                justify-content: center;
                align-items: center;
                height: 100%;
            }

            #loginBox {
                width: 300px;
                text-align: center;
                background-color: #ffffff;
            }
            .input-form-box {
                border: 0px solid #ff0000;
                display: flex;
                margin-bottom: 5px;
            }
            .input-form-box > span {
                display: block;
                text-align: left;
                padding-top: 5px;
                min-width: 65px;
            }
            .button-login-box {
                margin: 10px 0;
            }
            #loginBoxTitle {
                color:#000000;
                font-weight: bold;
                font-size: 32px;
                padding: 5px;
                margin-bottom: 20px;
                background: linear-gradient(to right, #270a09, #8ca6ce);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            #inputBox {
                margin: 10px;
            }
            #inputBox button {
                padding: 3px 5px;
            }
        </style>
    </head>
    <body>
        <?php
        if(isset($_POST["username"])){
            $username = $_POST["username"];
            if($username){
                $_SESSION['username'] = $username;
                echo "<script>alert('Login success.')</script><meta http-equiv=\"refresh\" content=\"0;url=/\" />";
            }
            else echo "<script>alert('Input username.')</script>";
        }
        ?>
        <div id="container">
            <div id="loginBox">
                <div id="loginBoxTitle">Login</div>
                <div id="inputBox">
                    <form  method="post">
                        <div class="input-form-box">
                            <span>Name</span>
                            <input type="text" name="username" class="form-control">
                        </div>
                        <div class="button-login-box" >
                            <input type="submit" class="btn btn-primary btn-xs" style="width:100%" value="Login">
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.min.js" integrity="sha384-mQ93GR66B00ZXjt0YO5KlohRA5SY2XofN4zfuZxLkoj1gXtW8ANNCe9d5Y3eG5eD" crossorigin="anonymous"></script>
    </body>
</html>