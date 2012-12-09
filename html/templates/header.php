<!DOCTYPE html>
<html>
<head>
	<!-- Some parts of this website are loosely based on the nascent CS50 Framework: http://cdn.cs50.net/2012/fall/psets/7/pset7.zip -->
    <meta http-equiv="Content-Type" charset="text/html; charset=UTF-8"/>

    <link href="css/bootstrap.css" rel="stylesheet"/>
    <link href="css/bootstrap-responsive.css" rel="stylesheet"/>
    <link href="css/styles.css" rel="stylesheet"/>
	<title>JPP: Jelle's Phylogeny Program<?= isset($data['title']) ? " – " . $data['title'] : '' ?></title>
    <script src="js/jquery-1.8.2.js"></script>
    <script src="js/bootstrap.js"></script>
    <script src="js/scripts.js"></script>
</head>
<body>

<h1>Jelle's Phylogeny Program</h1>
<div class="subtitle">Jelle Zijlstra, Harvard College, November&ndash;December 2012</div>
<ul id="navigation_list">
	<?php
		foreach($data['_links'] as $url => $link) {
			?>
				<a href="<?= $url ?>.php"><?= $link ?></a>
			<?php
		}
	?>
</ul>

<div id="container">
