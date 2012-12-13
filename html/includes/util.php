<?php
/*
 * Utility functions and configuration.
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

function render($template, $data = array()) {
	$data['_links'] = array(
		'index' => 'Home',
		'mp_intro' => 'Introduction to maximum parsimony',
	);

	require_once("templates/header.php");
	require_once("templates/" . $template . ".php");
	require_once("templates/footer.php");
}
