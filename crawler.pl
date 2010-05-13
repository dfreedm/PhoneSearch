#!/usr/bin/perl
# Daniel Freedman
# CS 410 Final Project
# Web forum crawler
# May 2010
use strict;
use warnings;
use utf8;
use WWW::Mechanize;
use List::MoreUtils qw(uniq);
use HTML::TreeBuilder;
use HTML::Tree;
use HTML::Element;
my @bases =
  qw(http://forums.precentral.net http://forum.tipb.com http://forum.androidcentral.com);

# Don't keep history (MUCH lower memory useage)
my $mech = WWW::Mechanize->new( stack_depth => 0 );

# Search each forum
for my $base (@bases) {

    # Search each board
    # Proper boards all have <strong> tags for names
    $mech->get($base);
    my @links = $mech->links();
    @links = map { $_->url() } @links;

    # Find where #top is, splits sections
    # Ugly hack, but it gets rid of the meta-boards
    my $i    = 0;
    my %tmp  = map { ( $i++ ) => $_ } @links;
    my @tops = grep { $tmp{$_} eq '#top' } keys %tmp;

    # delete tops and the following link from the links
    # Following link is a meta-board
    for (@tops) {
        delete $links[$_];
        delete $links[ ( $_ + 1 ) ];
    }

    # Grep out the undefs
    @links = grep { defined($_) } @links;

    # Only want links with style /word-word-.../
    # These are real boards
    my @topics = grep { m{^($base)?/[\w-]+/$} } @links;
    print "$_\n" for @topics;
    for my $topic (@topics) {

        # Search the first 1 .. n pages of threads
        for ( 1 .. 20 ) {
            print "$topic: page $_\n";
            unless ( $topic =~ m{$base} ) {
                $topic = $base . $topic;
            }
            $mech->get( $topic . "index$_.html" );

            # Grab the links
            my @links = $mech->links();

            # Only the url strings
            @links = map { $_->url() } @links;

            # Only want .html files
            @links = grep { m{/.*\.html$} } @links;

            # Ignore annoucements and other things
            @links =
              grep { $_ !~ m{-\d+\.html$|announcements|index|members} } @links;

            # Uniq links only pl0x
            @links = uniq(@links);

            # shift off the first four crap links
            shift @links for ( 1 .. 4 );

            # Iterate over links
            for my $link (@links) {
                unless ( $link =~ m{$base} ) {
                    $link = $base . $link;
                }

                $mech->get($link);

                # Take uri and give me a filename based on the path
                my $uri      = $mech->uri()->as_string();
                my $filename = ( $mech->uri()->path_segments() )[-1];
                $filename =~ s{html$}{txt};

                # Grab content
                my $content = $mech->content();
                my $text    = texify($content);
                my $next    = $mech->find_link( text_regex => qr/>/ );

                # Iterate over all pages in the thread
                while ($next) {
                    $mech->get( $next->url() );
                    $content = $mech->content();
                    $next    = $mech->find_link( text_regex => qr/>/ );
                    $text .= texify($content);
                }

                # Print the output to files
                open my ($out_post), ">", $filename;

                # Make UTF-8 characters print correctly
                binmode $out_post, ":utf8";
                print "filename: $filename\n";
                print $out_post $text . "\n";
                print $out_post $uri . "\n";
                close $out_post;
            }
        }
    }
}

# Take the input HTML, save only the post as parsed text
sub texify {
    my $content = shift;
    my $root    = HTML::TreeBuilder->new_from_content($content);

    # all posts are in divs where the id is of form "post_message_{number}"
    my @posts = $root->look_down( "id", qr/post_message_\d+/ );
    my $return = "";

    # String together all the posts
    foreach my $post (@posts) {
        $return .= ( $post->as_text() ) . "\n\n";
    }

    # Reduce memory useage
    $root->delete();
    return $return;
}
