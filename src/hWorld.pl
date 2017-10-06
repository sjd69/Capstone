=begin comment
Jordan Britton
This is a simple Hello World program
used to show that I've successfully
downloaded Perl and can create tests
using a built in package called the
Test Anything Protocol (TAP)
=cut
use Test::Simple tests => 6; #we can use Test::More to get more descriptive print outs of tests

#playing with hashes, learning data structures of Perl
my %testHarness = (
	'1' => "Jordan",
	'2' => "Alex",
	'3' => "Brianna",
	'4' => "Tyrone",
	'5' => "Tim",
	'6' => "Dave",
);
	
while( my($testString, $expect) = each %testHarness){
	my $thisString = "Hello World: $expect";
	ok($thisString eq "Hello World: $expect", "$expect Printed correctly");
}
