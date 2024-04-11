<?php
class Moon{
        public $name;
}
class Ion_Fan_Princess{
        public $nickname;
}

$a=new Moon();
$a->name=new Ion_Fan_Princess();
$a->name->nickname="小甜甜";
echo urlencode(serialize($a));
