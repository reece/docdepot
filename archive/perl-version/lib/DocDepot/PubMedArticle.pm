package DocDepot::PubMedArticle;

use Bio::DB::EUtilities;
use XML::Simple;

sub new {}
sub lookup {}


my $xml = get_record($pmid);
my $p = new XML::Simple(
  'ForceArray' => [ qw( AuthorList History ) ],
  'KeyAttr' => 0,
  'KeepRoot' => 0,
 );
my $dom = $p->XMLin($xml);
my $art = $dom->{PubmedArticle}->{MedlineCitation}->{Article};
bless($art,'Article');
