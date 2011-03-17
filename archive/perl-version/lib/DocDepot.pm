package DocDepot;

use Log::Log4perl;

my %defaults = (
  data_dir => '/srv/doc-depot',
 );


sub new {
  my $class = shift;
  my %self = ( %defaults, @_ );
  return bless($self,$class);
}

sub refile {
  my ($self,$src) = @_;
}

sub scan_incoming {}
sub pubmed_exists {}
