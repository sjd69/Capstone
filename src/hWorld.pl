=begin comment
Jordan Britton
This is a simple Hello World program
used to show that I've successfully
downloaded Perl and can create tests
using a built in package called the
Test Anything Protocol (TAP)
=cut
#!/usr/bin/perl
sub hello{
	$example = $_[0];
	return "Hello world: $example";
}
1;