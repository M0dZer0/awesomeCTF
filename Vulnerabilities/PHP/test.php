<?php
    highlight_file(__FILE__);
    function gettime($func, $p) {
        echo $func;
        echo $p;
        $result = call_user_func($func, $p);
        return $result;
    }

    class Test {
        public $p;
        public $func;
        public $disable_fun;

        function __destruct() {
            $disable_fun = array("exec","shell_exec","system","passthru","proc_open","show_source","phpinfo","popen","dl","eval","proc_terminate","touch","escapeshellcmd","escapeshellarg","assert","substr_replace","call_user_func_array","call_user_func","array_filter","array_walk");

            $func = strtolower($this->func);
            if (!in_array($func, $this->disable_fun)) {
                echo gettime($func, $this->p);
            } else {
                die("Hacker...");
            }
        }
    }

    $data = $_REQUEST["data"];
    $ppp = unserialize($data);
?>

