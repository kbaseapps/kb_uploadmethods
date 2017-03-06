package kb_uploadmethods::kb_uploadmethodsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_uploadmethods::kb_uploadmethodsClient

=head1 DESCRIPTION


A KBase module: kb_uploadmethods


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_uploadmethods::kb_uploadmethodsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my $token = Bio::KBase::AuthToken->new(@args);
	
	if (!$token->error_message)
	{
	    $self->{token} = $token->token;
	    $self->{client}->{token} = $token->token;
	}
        else
        {
	    #
	    # All methods in this module require authentication. In this case, if we
	    # don't have a token, we can't continue.
	    #
	    die "Authentication failed: " . $token->error_message;
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 upload_fastq_file

  $returnVal = $obj->upload_fastq_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_uploadmethods.UploadMethodParams
$returnVal is a kb_uploadmethods.UploadMethodResult
UploadMethodParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	fwd_staging_file_name has a value which is a kb_uploadmethods.fwd_staging_file_name
	rev_staging_file_name has a value which is a kb_uploadmethods.rev_staging_file_name
	download_type has a value which is a kb_uploadmethods.download_type
	fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
	rev_file_url has a value which is a kb_uploadmethods.rev_file_url
	sequencing_tech has a value which is a kb_uploadmethods.sequencing_tech
	name has a value which is a kb_uploadmethods.name
	urls_to_add has a value which is a kb_uploadmethods.urls_to_add
	single_genome has a value which is a kb_uploadmethods.single_genome
	interleaved has a value which is a kb_uploadmethods.interleaved
	insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
	insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
	read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward
workspace_name is a string
fwd_staging_file_name is a string
rev_staging_file_name is a string
download_type is a string
fwd_file_url is a string
rev_file_url is a string
sequencing_tech is a string
name is a string
urls_to_add is a reference to a hash where the following keys are defined:
	fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
	rev_file_url has a value which is a kb_uploadmethods.rev_file_url
	name has a value which is a kb_uploadmethods.name
	single_genome has a value which is a kb_uploadmethods.single_genome
	interleaved has a value which is a kb_uploadmethods.interleaved
	insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
	insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
	read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward
single_genome is a string
interleaved is a string
insert_size_mean is a string
insert_size_std_dev is a string
read_orientation_outward is a string
UploadMethodResult is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a kb_uploadmethods.obj_ref
	report_name has a value which is a kb_uploadmethods.report_name
	report_ref has a value which is a kb_uploadmethods.report_ref
obj_ref is a string
report_name is a string
report_ref is a string

</pre>

=end html

=begin text

$params is a kb_uploadmethods.UploadMethodParams
$returnVal is a kb_uploadmethods.UploadMethodResult
UploadMethodParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	fwd_staging_file_name has a value which is a kb_uploadmethods.fwd_staging_file_name
	rev_staging_file_name has a value which is a kb_uploadmethods.rev_staging_file_name
	download_type has a value which is a kb_uploadmethods.download_type
	fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
	rev_file_url has a value which is a kb_uploadmethods.rev_file_url
	sequencing_tech has a value which is a kb_uploadmethods.sequencing_tech
	name has a value which is a kb_uploadmethods.name
	urls_to_add has a value which is a kb_uploadmethods.urls_to_add
	single_genome has a value which is a kb_uploadmethods.single_genome
	interleaved has a value which is a kb_uploadmethods.interleaved
	insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
	insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
	read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward
workspace_name is a string
fwd_staging_file_name is a string
rev_staging_file_name is a string
download_type is a string
fwd_file_url is a string
rev_file_url is a string
sequencing_tech is a string
name is a string
urls_to_add is a reference to a hash where the following keys are defined:
	fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
	rev_file_url has a value which is a kb_uploadmethods.rev_file_url
	name has a value which is a kb_uploadmethods.name
	single_genome has a value which is a kb_uploadmethods.single_genome
	interleaved has a value which is a kb_uploadmethods.interleaved
	insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
	insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
	read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward
single_genome is a string
interleaved is a string
insert_size_mean is a string
insert_size_std_dev is a string
read_orientation_outward is a string
UploadMethodResult is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a kb_uploadmethods.obj_ref
	report_name has a value which is a kb_uploadmethods.report_name
	report_ref has a value which is a kb_uploadmethods.report_ref
obj_ref is a string
report_name is a string
report_ref is a string


=end text

=item Description



=back

=cut

 sub upload_fastq_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function upload_fastq_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to upload_fastq_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'upload_fastq_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_uploadmethods.upload_fastq_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'upload_fastq_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method upload_fastq_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'upload_fastq_file',
				       );
    }
}
 


=head2 unpack_staging_file

  $returnVal = $obj->unpack_staging_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_uploadmethods.UnpackStagingFileParams
$returnVal is a kb_uploadmethods.UnpackStagingFileOutput
UnpackStagingFileParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	staging_file_subdir_path has a value which is a string
workspace_name is a string
UnpackStagingFileOutput is a reference to a hash where the following keys are defined:
	unpacked_file_path has a value which is a string

</pre>

=end html

=begin text

$params is a kb_uploadmethods.UnpackStagingFileParams
$returnVal is a kb_uploadmethods.UnpackStagingFileOutput
UnpackStagingFileParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	staging_file_subdir_path has a value which is a string
workspace_name is a string
UnpackStagingFileOutput is a reference to a hash where the following keys are defined:
	unpacked_file_path has a value which is a string


=end text

=item Description

Unpack a staging area file

=back

=cut

 sub unpack_staging_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function unpack_staging_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to unpack_staging_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'unpack_staging_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_uploadmethods.unpack_staging_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'unpack_staging_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method unpack_staging_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'unpack_staging_file',
				       );
    }
}
 


=head2 unpack_web_file

  $returnVal = $obj->unpack_web_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_uploadmethods.UnpackWebFileParams
$returnVal is a kb_uploadmethods.UnpackWebFileOutput
UnpackWebFileParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	file_url has a value which is a string
	download_type has a value which is a string
	urls_to_add_web_unpack has a value which is a kb_uploadmethods.urls_to_add_web_unpack
workspace_name is a string
urls_to_add_web_unpack is a reference to a hash where the following keys are defined:
	file_url has a value which is a string
UnpackWebFileOutput is a reference to a hash where the following keys are defined:
	unpacked_file_path has a value which is a string

</pre>

=end html

=begin text

$params is a kb_uploadmethods.UnpackWebFileParams
$returnVal is a kb_uploadmethods.UnpackWebFileOutput
UnpackWebFileParams is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_uploadmethods.workspace_name
	file_url has a value which is a string
	download_type has a value which is a string
	urls_to_add_web_unpack has a value which is a kb_uploadmethods.urls_to_add_web_unpack
workspace_name is a string
urls_to_add_web_unpack is a reference to a hash where the following keys are defined:
	file_url has a value which is a string
UnpackWebFileOutput is a reference to a hash where the following keys are defined:
	unpacked_file_path has a value which is a string


=end text

=item Description

Download and unpack a web file to staging area

=back

=cut

 sub unpack_web_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function unpack_web_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to unpack_web_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'unpack_web_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_uploadmethods.unpack_web_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'unpack_web_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method unpack_web_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'unpack_web_file',
				       );
    }
}
 


=head2 import_genbank_from_staging

  $returnVal = $obj->import_genbank_from_staging($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_uploadmethods.GenbankToGenomeParams
$returnVal is a kb_uploadmethods.GenomeSaveResult
GenbankToGenomeParams is a reference to a hash where the following keys are defined:
	staging_file_subdir_path has a value which is a string
	genome_name has a value which is a string
	workspace_name has a value which is a string
	source has a value which is a string
	release has a value which is a string
	genetic_code has a value which is an int
	type has a value which is a string
	generate_ids_if_needed has a value which is a string
GenomeSaveResult is a reference to a hash where the following keys are defined:
	genome_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_uploadmethods.GenbankToGenomeParams
$returnVal is a kb_uploadmethods.GenomeSaveResult
GenbankToGenomeParams is a reference to a hash where the following keys are defined:
	staging_file_subdir_path has a value which is a string
	genome_name has a value which is a string
	workspace_name has a value which is a string
	source has a value which is a string
	release has a value which is a string
	genetic_code has a value which is an int
	type has a value which is a string
	generate_ids_if_needed has a value which is a string
GenomeSaveResult is a reference to a hash where the following keys are defined:
	genome_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub import_genbank_from_staging
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function import_genbank_from_staging (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to import_genbank_from_staging:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'import_genbank_from_staging');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_uploadmethods.import_genbank_from_staging",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'import_genbank_from_staging',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method import_genbank_from_staging",
					    status_line => $self->{client}->status_line,
					    method_name => 'import_genbank_from_staging',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_uploadmethods.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_uploadmethods.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'import_genbank_from_staging',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method import_genbank_from_staging",
            status_line => $self->{client}->status_line,
            method_name => 'import_genbank_from_staging',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_uploadmethods::kb_uploadmethodsClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_uploadmethods::kb_uploadmethodsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 workspace_name

=over 4



=item Description

workspace name of the object


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 fwd_staging_file_name

=over 4



=item Description

input and output file path/url


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 rev_staging_file_name

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 download_type

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 fwd_file_url

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 rev_file_url

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 sequencing_tech

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 name

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 single_genome

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 interleaved

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 insert_size_mean

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 insert_size_std_dev

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 read_orientation_outward

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 obj_ref

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 report_name

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 report_ref

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 urls_to_add

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
rev_file_url has a value which is a kb_uploadmethods.rev_file_url
name has a value which is a kb_uploadmethods.name
single_genome has a value which is a kb_uploadmethods.single_genome
interleaved has a value which is a kb_uploadmethods.interleaved
insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
rev_file_url has a value which is a kb_uploadmethods.rev_file_url
name has a value which is a kb_uploadmethods.name
single_genome has a value which is a kb_uploadmethods.single_genome
interleaved has a value which is a kb_uploadmethods.interleaved
insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward


=end text

=back



=head2 UploadMethodParams

=over 4



=item Description

sequencing_tech: sequencing technology
name: output reads file name
workspace_name: workspace name/ID of the object

For files in user's staging area:
fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
rev_staging_file_name: reverse/right paired-end fastq file name user's staging area

For files from web:
download_type: download type for web source fastq file ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
rev_file_url: reverse/right paired-end fastq file URL
 
urls_to_add: used for parameter-groups. dict of {fwd_file_url, rev_file_url, name,
                        single_genome, interleaved, insert_size_mean and read_orientation_outward}

Optional Params:
single_genome: whether the reads are from a single genome or a metagenome.
    interleaved: whether reads is interleaved
    insert_size_mean: mean (average) insert length
    insert_size_std_dev: standard deviation of insert lengths
    read_orientation_outward: whether reads in a pair point outward


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
fwd_staging_file_name has a value which is a kb_uploadmethods.fwd_staging_file_name
rev_staging_file_name has a value which is a kb_uploadmethods.rev_staging_file_name
download_type has a value which is a kb_uploadmethods.download_type
fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
rev_file_url has a value which is a kb_uploadmethods.rev_file_url
sequencing_tech has a value which is a kb_uploadmethods.sequencing_tech
name has a value which is a kb_uploadmethods.name
urls_to_add has a value which is a kb_uploadmethods.urls_to_add
single_genome has a value which is a kb_uploadmethods.single_genome
interleaved has a value which is a kb_uploadmethods.interleaved
insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
fwd_staging_file_name has a value which is a kb_uploadmethods.fwd_staging_file_name
rev_staging_file_name has a value which is a kb_uploadmethods.rev_staging_file_name
download_type has a value which is a kb_uploadmethods.download_type
fwd_file_url has a value which is a kb_uploadmethods.fwd_file_url
rev_file_url has a value which is a kb_uploadmethods.rev_file_url
sequencing_tech has a value which is a kb_uploadmethods.sequencing_tech
name has a value which is a kb_uploadmethods.name
urls_to_add has a value which is a kb_uploadmethods.urls_to_add
single_genome has a value which is a kb_uploadmethods.single_genome
interleaved has a value which is a kb_uploadmethods.interleaved
insert_size_mean has a value which is a kb_uploadmethods.insert_size_mean
insert_size_std_dev has a value which is a kb_uploadmethods.insert_size_std_dev
read_orientation_outward has a value which is a kb_uploadmethods.read_orientation_outward


=end text

=back



=head2 UploadMethodResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a kb_uploadmethods.obj_ref
report_name has a value which is a kb_uploadmethods.report_name
report_ref has a value which is a kb_uploadmethods.report_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a kb_uploadmethods.obj_ref
report_name has a value which is a kb_uploadmethods.report_name
report_ref has a value which is a kb_uploadmethods.report_ref


=end text

=back



=head2 UnpackStagingFileParams

=over 4



=item Description

Input parameters for the "unpack_staging_file" function.

      Required parameters:
      staging_file_subdir_path: subdirectory file path
      e.g. 
        for file: /data/bulk/user_name/file_name
        staging_file_subdir_path is file_name
        for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
        staging_file_subdir_path is subdir_1/subdir_2/file_name
      workspace_name: workspace name/ID of the object


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
staging_file_subdir_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
staging_file_subdir_path has a value which is a string


=end text

=back



=head2 UnpackStagingFileOutput

=over 4



=item Description

Results from the unpack_staging_file function.

      unpacked_file_path: unpacked file path(s) in staging area


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
unpacked_file_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
unpacked_file_path has a value which is a string


=end text

=back



=head2 urls_to_add_web_unpack

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
file_url has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
file_url has a value which is a string


=end text

=back



=head2 UnpackWebFileParams

=over 4



=item Description

Input parameters for the "unpack_web_file" function.

      Required parameters:
      workspace_name: workspace name/ID of the object
      file_url: file URL
      download_type: one of ['Direct Download', 'FTP', 'DropBox', 'Google Drive']

      Optional:
      urls_to_add_web_unpack: used for parameter-groups. dict of {file_url}


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
file_url has a value which is a string
download_type has a value which is a string
urls_to_add_web_unpack has a value which is a kb_uploadmethods.urls_to_add_web_unpack

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_uploadmethods.workspace_name
file_url has a value which is a string
download_type has a value which is a string
urls_to_add_web_unpack has a value which is a kb_uploadmethods.urls_to_add_web_unpack


=end text

=back



=head2 UnpackWebFileOutput

=over 4



=item Description

Results from the unpack_web_file function.

      unpacked_file_path: unpacked file path(s) in staging area


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
unpacked_file_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
unpacked_file_path has a value which is a string


=end text

=back



=head2 GenbankToGenomeParams

=over 4



=item Description

import_genbank_from_staging: wrapper method for GenomeFileUtil.genbank_to_genome

  required params:
  staging_file_subdir_path - subdirectory file path
  e.g. 
    for file: /data/bulk/user_name/file_name
    staging_file_subdir_path is file_name
    for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
    staging_file_subdir_path is subdir_1/subdir_2/file_name
  genome_name - becomes the name of the object
  workspace_name - the name of the workspace it gets saved to.
  source - Source of the file typically something like RefSeq or Ensembl

  optional params:
  release - Release or version number of the data 
      per example Ensembl has numbered releases of all their data: Release 31
  generate_ids_if_needed - If field used for feature id is not there, 
      generate ids (default behavior is raising an exception)
  genetic_code - Genetic code of organism. Overwrites determined GC from 
      taxon object
  type - Reference, Representative or User upload


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
staging_file_subdir_path has a value which is a string
genome_name has a value which is a string
workspace_name has a value which is a string
source has a value which is a string
release has a value which is a string
genetic_code has a value which is an int
type has a value which is a string
generate_ids_if_needed has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
staging_file_subdir_path has a value which is a string
genome_name has a value which is a string
workspace_name has a value which is a string
source has a value which is a string
release has a value which is a string
genetic_code has a value which is an int
type has a value which is a string
generate_ids_if_needed has a value which is a string


=end text

=back



=head2 GenomeSaveResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
genome_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
genome_ref has a value which is a string


=end text

=back



=cut

package kb_uploadmethods::kb_uploadmethodsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
