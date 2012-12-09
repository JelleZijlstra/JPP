<?php
/*
 * Utility functions and configuration.
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);



function render($template, $data) {
	$data['_links'] = array(
		'index' => 'Home',

	);

	require_once("templates/header.php");
	require_once("templates/" . $template . ".php");
	require_once("templates/footer.php");
}
