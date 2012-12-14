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
		'run_mp' => 'Run an MP search yourself',
		'documentation' => 'Documentation',
		'design' => 'Design and performance',
		'issues' => 'Issues and areas for improvement',
		'background' => 'Background and personal evaluation',
	);

	require_once("templates/header.php");
	require_once("templates/" . $template . ".php");
	require_once("templates/footer.php");
}
