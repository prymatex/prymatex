package beautify;

use Exporter;
@EXPORT = qw( js_beautify );
@ISA 		= qw( Exporter ); 


use strict;

use constant IN_EXPR			=>  2;
use constant IN_BLOCK			=>  3;

use constant TK_UNKNOWN			=>  4;
use constant TK_WORD			=>  5;
use constant TK_START_EXPR		=>  6;
use constant TK_END_EXPR		=>  7;
use constant TK_START_BLOCK		=>  8;
use constant TK_END_BLOCK		=>  9;
use constant TK_END_COMMAND		=> 10;
use constant TK_EOF			=> 11;
use constant TK_STRING			=> 12;

use constant TK_BLOCK_COMMENT	=> 13;
use constant TK_COMMENT			=> 14;

use constant TK_OPERATOR		=> 15;

# internal flags
use constant PRINT_NONE			=> 16;
use constant PRINT_SPACE		=> 17;
use constant PRINT_NL			=> 18;

use constant WHITESPACE			=> split('', "\n\r\t ");
use constant WORDCHAR			=> split('','abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$');
use constant PUNCT				=> split(' ', '+ - * / % & ++ -- = += -= *= /= %= == === != !== > < >= <= >> << >>> >>>= >>= <<= && &= | || ! !! , : ? ^ ^= |='); 

my $indent;
my $output;
my $tab_string;
my $token_text;
my @ins;
my $in;
my $last_type;
my $last_text;
my $input;
my $input_length;


sub nl($)
{
	my ($ignore_repeated) = @_;
	$output =~ s/ +$//g;
	if ($output ne '')
	{
		$output.="\n" unless $ignore_repeated && substr($output,-1) eq "\n";
		$output .= $tab_string x $indent;
	}
}

sub space()
{
	if ($output ne '' && substr($output, -1) ne ' ')
	{
		$output .= ' ';
	}
}

sub indent()
{
	$indent++;
}

sub unindent()
{
	$indent-- if $indent;
}

sub token()
{
	$output .= $token_text;
}

sub remove_indent()
{
	my $tab_len = length $tab_string;
	$output = substr($output, 0, -$tab_len) if substr($output,-$tab_len) eq $tab_string;	
}

sub in($)
{
	push @ins, $in;
	$in = @_[0];
}

sub in_pop()
{
	$in = pop @ins;
}

sub get_next_token($)
{
	my ($ppos) = @_;

	my $n_newlines = 0;
	my $c;
    do {
        if ($$ppos >= $input_length) {
            return ['', TK_EOF];
        }
        $c = substr($input,$$ppos,1);
        $$ppos++;
        if ($c eq "\n") {
            nl($n_newlines == 0);
            $n_newlines++;
        }
    } while (grep {$_ eq $c} (WHITESPACE));

    if (grep {$_ eq $c} (WORDCHAR)) {
        if ($$ppos < $input_length) {
        	my $cc = substr($input, $$ppos, 1);
            while (grep {$_ eq $cc} (WORDCHAR)) {
                $c .= $cc;
                $$ppos++;
                last if ($$ppos == $input_length);
	        	$cc = substr($input, $$ppos, 1);
            }
        }

        # small and surprisingly unugly hack for 1E-10 representation
        if ($$ppos != $input_length && $c =~ m/^\d+[Ee]$/ && substr($input, $$ppos, 1) eq '-') {
            $$ppos++;
            my ($next_word, $next_type) = get_next_token($ppos);
            $c .= '-' . $next_word;
            return [$c, TK_WORD];
        }
        
        if ($c eq 'in') { # hack for 'in' operator
            return [$c, TK_OPERATOR];
        }
        return [$c, TK_WORD];
    }

    if ($c eq '(' || $c eq '[') {
        return [$c, TK_START_EXPR];
    }

    if ($c eq ')' || $c eq ']') {
        return [$c, TK_END_EXPR];
    }

    if ($c eq '{') {
        return [$c, TK_START_BLOCK];
    }

    if ($c eq '}') {
        return [$c, TK_END_BLOCK];
    }

    if ($c eq ';') {
        return [$c, TK_END_COMMAND];
    }

    if ($c eq '/') {
        # peek for comment /* ... */
        if (substr($input, $$ppos, 1) eq '*') {
            my $comment = '';
            $$ppos++;
            if ($$ppos < $input_length){
                while (substr($input, $$ppos, 2) ne '*/' && $$ppos < $input_length) {
                    $comment .= substr($input, $$ppos, 1);
                    $$ppos++;
                }
            }
            $$ppos += 2;
            return ["/*$comment*/", TK_BLOCK_COMMENT];
        }
        # peek for comment // ...
        if (substr($input, $$ppos, 1) eq '/') {
            my $comment = $c;
            while (substr($input, $$ppos, 1) ne "\x0d" && substr($input, $$ppos, 1) ne "\x0a") {
                $comment .= substr($input, $$ppos, 1);
                $$ppos++;
                last if ($$ppos >= $input_length);
            }
            $$ppos++;
            return [$comment, TK_COMMENT];
        }
    }

    if ($c eq "'" || # string
        $c eq '"' || # string
        ($c eq '/' && 
            (($last_type == TK_WORD and $last_text eq 'return') or ($last_type == TK_START_EXPR || $last_type == TK_END_BLOCK || $last_type == TK_OPERATOR || $last_type == TK_EOF || $last_type == TK_END_COMMAND)))) { # regexp
        my $sep = $c;
    	$c   = '';
        my $esc = 0;

        if ($$ppos < $input_length) {
            while ($esc || substr($input, $$ppos, 1) ne $sep) {
                $c .= substr($input, $$ppos, 1);
                if (!$esc) {
                    $esc = (substr($input, $$ppos, 1) eq "\\");
                } else {
                    $esc = 0;
                }
                $$ppos++;
                last if ($$ppos >= $input_length);
            }
        }

        $$ppos++;
        if ($last_type == TK_END_COMMAND) {
            nl(1);
        }
        return [$sep . $c . $sep, TK_STRING];
    }

    if (grep {$_ eq $c} (PUNCT)) {
        while ($$ppos < $input_length)
        {
        	my $cc = substr($input, $$ppos, 1);
            if (grep {$_ eq $c.$cc} (PUNCT))
            {
	        	$c .= $cc;
            	$$ppos += 1;
	            last if ($$ppos >= $input_length);
            } else {
            	last;
            }
        }
        return [$c, TK_OPERATOR];
    }

    return [$c, TK_UNKNOWN];
}

sub js_beautify($$)
{
	my ($js_source, $tab_size) = @_;
	
	$input = $js_source;
	$input_length = length $input;
	
	$tab_string = ' ' x $tab_size;

    my $last_word = '';            # last TK_WORD passed
    $last_type = TK_START_EXPR; # last token type
    $last_text = '';            # last token text
    $output    = '';

    # words which should always start on new line. 
    # simple hack for cases when lines aren't ending with semicolon.
    # feel free to tell me about the ones that need to be added. 
    my @line_starters = qw(continue try throw return var if switch case default for while break function);

    # states showing if we are currently in expression (i.e. "if" case) - IN_EXPR, or in usual block (like, procedure), IN_BLOCK.
    # some formatting depends on that.
    $in       = IN_BLOCK;
    @ins      = [$in];


    $indent   = 0;
    my $pos      = 0; # parser position
    my $in_case  = 0; # flag for parser that case/default has been processed, and next colon needs special attention

    while (1) {
    	my $token_type;
        ($token_text, $token_type) = @{get_next_token(\$pos)};
        last if $token_type == TK_EOF;

        # $output .= " [$token_type:$last_type]";

		if ($token_type == TK_START_EXPR)
		{
			in(IN_EXPR);
            if ($last_type == TK_END_EXPR or $last_type == TK_START_EXPR) {
                # do nothing on (( and )( and ][ and ]( .. 
            } elsif ($last_type != TK_WORD and $last_type != TK_OPERATOR) {
                space();
            } elsif (grep {$_ eq $last_word} @line_starters and $last_word ne 'function') { 
                space();
            }
            token();
		} elsif ($token_type == TK_END_EXPR)
		{
            token();
            in_pop();
		} elsif ($token_type == TK_START_BLOCK)
		{
            in(IN_BLOCK);
            if ($last_type != TK_OPERATOR and $last_type != TK_START_EXPR) {
                if ($last_type == TK_START_BLOCK) {
                    nl(1);
                } else {
                    space();
                }
            }
            token();
            indent();
		} elsif ($token_type == TK_END_BLOCK)
		{
            if ($last_type == TK_END_EXPR) {
                unindent();
                nl(1);
            } elsif ($last_type == TK_END_BLOCK) {
                unindent();
                nl(1);
            } elsif ($last_type == TK_START_BLOCK) {
                # nothing
                unindent();
            } else {
                unindent();
                nl(1);
            }
            token();
            in_pop();
		} elsif ($token_type == TK_WORD)
		{
            if ($token_text eq 'case' or $token_text eq 'default') {
                if ($last_text eq ':') {
                    # switch cases following one another
                    remove_indent();
                } else {
                    $indent--;
                    nl(1);
                    $indent++;
                }
                token();
                $in_case = 1;
            } else {
	            my $prefix = PRINT_NONE;
	            if ($last_type == TK_END_BLOCK) {
	                if ($token_text eq 'else' or $token_text eq 'catch' or $token_text eq 'finally') {
	                    $prefix = PRINT_SPACE;
	                    space();
	                } else {
	                    $prefix = PRINT_NL;
	                }
	            } elsif ($last_type == TK_END_COMMAND && $in == IN_BLOCK) {
	                $prefix = PRINT_NL;
	            } elsif ($last_type == TK_END_COMMAND && $in == IN_EXPR) {
	                $prefix = PRINT_SPACE;
	            } elsif ($last_type == TK_WORD) {
	                if ($last_word eq 'else') { # else if
	                    $prefix = PRINT_SPACE;
	                } else {
	                    $prefix = PRINT_SPACE; 
	                }
	            } elsif ($last_type == TK_START_BLOCK) {
	                $prefix = PRINT_NL;
	            } elsif ($last_type == TK_END_EXPR) {
	                space();
	            }
	
	            if (grep {$_ eq $token_text} @line_starters or $prefix == PRINT_NL) {
	
	                if ($last_text eq 'else') {
	                    # no need to force newline on else break
	                    # DONOTHING
	                    space();
	                } elsif (($last_type == TK_START_EXPR or $last_text eq '=') and $token_text eq 'function') {
	                    # no need to force newline on 'function': (function
	                    # DONOTHING
	                } elsif ($last_type eq TK_WORD and ($last_text eq 'return' or $last_text eq 'throw')) {
	                    # no newline between 'return nnn'
	                    space();
	                } else
	                {
	                    if ($last_type != TK_END_EXPR) {
	                        if (($last_type != TK_START_EXPR or $token_text ne 'var') and $last_text ne ':') { 
	                            # no need to force newline on 'var': for (var x = 0...)
	                            if ($token_text eq 'if' and $last_type == TK_WORD and $last_word eq 'else') {
	                                # no newline for } else if {
	                                space();
	                            } else {
	                                nl(1);
	                            }
	                        }
	                    }
                    }
	            } elsif ($prefix == PRINT_SPACE) {
	                space();
	            }
	            token();
	            $last_word = $token_text;
            }
		} elsif ($token_type == TK_END_COMMAND)
		{
            token();
		} elsif ($token_type == TK_STRING)
		{
            if ($last_type == TK_START_BLOCK or $last_type == TK_END_BLOCK) {
                nl(1);
            } elsif ($last_type == TK_WORD) {
                space();
            }
            token();
		} elsif ($token_type == TK_OPERATOR)
		{
            my $start_delim = 1;
            my $end_delim   = 1;

            if ($token_text eq ':' and $in_case) {
                token(); # colon really asks for separate treatment
                nl(1);
                # $expecting_case = 0;
            } else
            {
	            $in_case = 0;
	            if ($token_text eq ',') {
	                if ($last_type == TK_END_BLOCK) {
	                    token();
	                    nl(1);
	                } else {
	                    if ($in == IN_BLOCK) {
	                        token();
	                        nl(1);
	                    } else {
	                        token();
	                        space();
	                    }
	                }
	            } else
	            {
		            if ($token_text eq '--' or $token_text eq '++') { # unary operators special case
		                if ($last_text eq ';') {
		                    # space for (;; ++i)  
		                    $start_delim = 1;
		                    $end_delim = 0;
		                } else {                
		                    $start_delim = 0;
		                    $end_delim = 0;
		                }
		            } elsif ($token_text eq '!' and $last_type == TK_START_EXPR) {
		                # special case handling: if (!a)
		                $start_delim = 0;
		                $end_delim = 0;
		            } elsif ($last_type == TK_OPERATOR) {
		                $start_delim = 0;
		                $end_delim = 0;
		            } elsif ($last_type == TK_END_EXPR) {
		                $start_delim = 1;
		                $end_delim = 1;
		            } elsif ($token_text eq '.') {
		                # decimal digits or object.property
		                $start_delim = 0;
		                $end_delim   = 0;
		
		            } elsif ($token_text eq ':') {
		                # zz: xx
		                # can't differentiate ternary op, so for now it's a ? b: c; without space before colon
		                $start_delim = 0;
		            }
		            if ($start_delim) {
		                space();
		            }
		
		            token();
		            
		            if ($end_delim) {
		                space();
		            }
            	}
            }
		} elsif ($token_type == TK_BLOCK_COMMENT)
		{
            nl(1);
            token();
            nl(1);
		} elsif ($token_type == TK_COMMENT)
		{
            #if ($last_type != TK_COMMENT) {
            nl(1);
            #}
            token();
            nl(1);
		} elsif ($token_type == TK_UNKNOWN)
		{
            token();
        }

        if ($token_type != TK_COMMENT) {
            $last_type = $token_type;
            $last_text = $token_text;
        }
    }

    # clean empty lines from redundant spaces
    $output =~ s/^ +$//m;

    return $output;
}

1;