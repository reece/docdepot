package DocDepot::PubMedFiler;

use strict;
use warnings;

use base 'DocDepot::Filer';

use DocDepot::PubMedArticle;


my @refilers = (
  # name         dir		 fnfn
  [ 'PubMed id'			, 'pmid'		, \&by_pmid 		],
  [ 'PubMed id, 3x2'	, 'pmid-3x2'	, \&by_pmid_3x2 	],
  [ 'Authors'			, 'author'		, \&by_authors 		],
  [ 'Locus'				, 'locus'		, \&by_locus 		],
);




foreach my $refiler (@refilers) {
  my ($name,$dir,$fnfn) = @$refiler;
  my $sfx = suffix($pdf_fn) || '';
  my @paths = map { "$dir/$_$sfx" } &$fnfn($pdf_fn,$pmid,$art);
  print( "* $name\n", map { "  $_\n" } @paths );
}

exit;



sub by_pmid {
  my ($fn,$pmid,$art) = @_;
  return $pmid;
}

sub by_pmid_3x2 {
  my ($fn,$pmid,$art) = @_;
  my @s = $pmid =~ m/(\d\d)(\d\d)(\d\d)/;
  return( join('/',@s[0..2],$pmid) );
}

sub by_authors {
  my ($fn,$pmid,$art) = @_;
  my $ymd = $art->ymd;
  my $title = $art->title;
  map {"$_/$ymd $title"} $art->authors;
}

sub by_locus {
  my ($fn,$pmid,$art) = @_;
  my $ymd = $art->ymd;
  my $title = $art->title;
  my @authors = $art->authors;
  my $au = $authors[0];
  $au =~ s/\s+//;
  sprintf("%s_%s_%s_%s", $pmid, $art->year, $art->jrnl, $au);

}



sub get_record {
  my $pmid = shift;
  my $f = Bio::DB::EUtilities->new(-eutil => 'efetch',
								   -db => 'pubmed',
								   -id => $pmid);
  return $f->get_Response->content();
}

sub suffix {
  $_[0] =~ m/(.\w{1,5})$/ && return $1;
}



BEGIN {

package Article;
sub title { my $x = $_[0]->{ArticleTitle}; $x =~ s/\.//; $x; }
sub authors { map { __au_LastFM($_) } @{$_[0]->{AuthorList}}; }
sub jrnl { $_[0]->{Journal}->{ISOAbbreviation} }
sub year { $_[0]->{ArticleDate}->{Year} }
sub ymd { join('-', @{$_[0]->{ArticleDate}}{qw(Year Month Day)} ) }

sub __au_LastFM { "$_[0]->{Author}->{LastName} $_[0]->{Author}->{Initials}"; }
}
