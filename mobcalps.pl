#/usr/bin/perl
use Digest::MD5 qw(md5_hex); use File::Copy;
####THIS SOFTWARE COMES WITH ABSOLUTELY NO WARRANTY! READ THE LICENSE##########
print "\nCopyright (c) 2011, J.P. Boyd. All rights reserved.\n";
$dash="===============================================================================\n";
$reddash=$dash;
$note="\n==NOTE:========================================================================\n";
$warning= "\n==WARNING:=====================================================================\a\a\n";
$timefiller="\n==READ WHILE WAITING:==========================================================\n";
$failed= "FAILED";
################################## LICENSE ####################################
if (($ARGV[0] =~ "c") or (not -e 'config.cfg')){
print $dash;
print "                          The \"Artistic License\"\n";
print $dash;
print "PRESS RETURN"; $kill=<STDIN>; print "\n";
print <<ARTISTIC

Preamble

The intent of this document is to state the conditions under which a
Package may be copied, such that the Copyright Holder maintains some
semblance of artistic control over the development of the package,
while giving the users of the package the right to use and distribute
the Package in a more-or-less customary fashion, plus the right to make
reasonable modifications.

Definitions:

	"Package" refers to the collection of files distributed by the
	Copyright Holder, and derivatives of that collection of files
	created through textual modification.

	"Standard Version" refers to such a Package if it has not been
	modified, or has been modified in accordance with the wishes
	of the Copyright Holder as specified below.

	"Copyright Holder" is whoever is named in the copyright or
	copyrights for the package.

	"You" is you, if you're thinking about copying or distributing
	this Package.

	"Reasonable copying fee" is whatever you can justify on the
	basis of media cost, duplication charges, time of people involved,
	and so on.  (You will not be required to justify it to the
	Copyright Holder, but only to the computing community at large
	as a market that must bear the fee.)

	"Freely Available" means that no fee is charged for the item
	itself, though there may be fees involved in handling the item.
	It also means that recipients of the item may redistribute it
	under the same conditions they received it.

1. You may make and give away verbatim copies of the source form of the
Standard Version of this Package without restriction, provided that you
duplicate all of the original copyright notices and associated disclaimers.

2. You may apply bug fixes, portability fixes and other modifications
derived from the Public Domain or from the Copyright Holder.  A Package
modified in such a way shall still be considered the Standard Version.

3. You may otherwise modify your copy of this Package in any way, provided
that you insert a prominent notice in each changed file stating how and
when you changed that file, and provided that you do at least ONE of the
following:

    a) place your modifications in the Public Domain or otherwise make them
    Freely Available, such as by posting said modifications to Usenet or
    an equivalent medium, or placing the modifications on a major archive
    site such as uunet.uu.net, or by allowing the Copyright Holder to include
    your modifications in the Standard Version of the Package.

    b) use the modified Package only within your corporation or organization.

    c) rename any non-standard executables so the names do not conflict
    with standard executables, which must also be provided, and provide
    a separate manual page for each non-standard executable that clearly
    documents how it differs from the Standard Version.

    d) make other distribution arrangements with the Copyright Holder.

4. You may distribute the programs of this Package in object code or
executable form, provided that you do at least ONE of the following:

    a) distribute a Standard Version of the executables and library files,
    together with instructions (in the manual page or equivalent) on where
    to get the Standard Version.

    b) accompany the distribution with the machine-readable source of
    the Package with your modifications.

    c) give non-standard executables non-standard names, and clearly
    document the differences in manual pages (or equivalent), together
    with instructions on where to get the Standard Version.

    d) make other distribution arrangements with the Copyright Holder.

5. You may charge a reasonable copying fee for any distribution of this
Package.  You may charge any fee you choose for support of this
Package.  You may not charge a fee for this Package itself.  However,
you may distribute this Package in aggregate with other (possibly
commercial) programs as part of a larger (possibly commercial) software
distribution provided that you do not advertise this Package as a
product of your own.  You may embed this Package's interpreter within
an executable of yours (by linking); this shall be construed as a mere
form of aggregation, provided that the complete Standard Version of the
interpreter is so embedded.

6. The scripts and library files supplied as input to or produced as
output from the programs of this Package do not automatically fall
under the copyright of this Package, but belong to whoever generated
them, and may be sold commercially, and may be aggregated with this
Package.  If such scripts or library files are aggregated with this
Package via the so-called "undump" or "unexec" methods of producing a
binary executable image, then distribution of such an image shall
neither be construed as a distribution of this Package nor shall it
fall under the restrictions of Paragraphs 3 and 4, provided that you do
not represent such an executable image as a Standard Version of this
Package.

7. C subroutines (or comparably compiled subroutines in other
languages) supplied by you and linked into this Package in order to
emulate subroutines and variables of the language defined by this
Package shall not be considered part of this Package, but are the
equivalent of input as in Paragraph 6, provided these subroutines do
not change the language in any way that would cause it to fail the
regression tests for the language.

8. Aggregation of this Package with a commercial distribution is always
permitted provided that the use of this Package is embedded; that is,
when no overt attempt is made to make this Package's interfaces visible
to the end user of the commercial distribution.  Such use shall not be
construed as a distribution of this Package.

9. The name of the Copyright Holder may not be used to endorse or promote
products derived from this software without specific prior written permission.

19. THIS SOFTWARE IS PROVIDED BY J.P: BOYD "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL J.P. Boyd BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

                                The End
                                
ARTISTIC
; if (not $ARGV[0]=~"c"){
print "DO YOU AGREE TO THE TERMS SPECIFIED IN THE LICENSE [YES/no]? ";
$kill=<STDIN>;
if ($kill=~"no"){goto KILL}
} else {goto KILL}
}
################################## License#####################################
if ($ARGV[0] =~ "h"){
(print <<CMDNOTES

====================== mobcalPARSER v0.0.1 (artistic) ==========================
uses:
Digest::MD5
File::Copy
Term::ANSIColor
                             # RELEASE NOTES #

  "MOBCAL - A Program to Calculate Mobilities" is the intellectual property
  of Professor Martin F. Jarrold. The fortran77 source code is available
  free of charge at http://www.indiana.edu/~nano/software.html.
  
  citations: M. F. Mesleh, J. M. Hunter, A. A. Shvartsburg, G. C. Schatz
  and M. F. Jarrold, J. Phys. Chem. 1996, 100, 16082-16086; Erratum,
  J. Phys. Chem. A 1997, 101, 968. A. A. Shvartsburg and M. F. Jarrold,
  Chem. Phys. Lett. 1996, 261, 86-91.

  mobcalPARSER is a PERL frontend, the original MOBCAL fortran77 code is not
  contained in the standard package (cf. "artistic license"), you can download
  the source from the address provided above (build 06/15/00). To compile
  MOBCAL you can use e.g. Force 2.0.9 (win32) or
  gfortran (gfortran -std=legacy).

  mobcalPARSER v0.0.1 was tested in combination with:

  > Orca 2.7.0 & 2.8.0;
  > Gaussian 94, 98, 03 & 09;
  > .xyz and .mol
  
  The frontend runs on linux and win32, but it's preconfigured for win32.
  Under linux you have to change config.cfg. There is a line initially called
  'mobcal.exe", change it to "./mobcal", where "./mobcal" is the compiled
  MOBCAL program (use chmod +x ..).
  
  This is EXPERIMENTAL SOFTWARE and COMES WITH ABSOLUTELY NO WARRANTY, read
  the license (license is present in source and printed on screen when you
  run the frontend for the first time, set 'c' switch to read it on screen
  later on).

== AUTOMATIC PROCESSING =======================================================

  By default (i.e. calling the script without switches) files in the working
  directory are processed automatically. You can simply copy the file(s)
  you want to pass through into the working directory and run the program
  by 'double-clicking' mobcalPARSER.pl. The following hierarchy applies for
  automatic processing:
  
  > *.out FILES ARE TREATED AS ORCA OUTPUT
  > *.log FILES ARE TREATED AS GAUSSIAN OUTPUT
  > *.xyz FILES ARE TREATED AS XYZ GEOMETRY
  > *.mol FILES ARE TREATED AS MDL MOL GEOMETRY

  Therefore, .log files are ignored as long as .out files are present, while
  .xyz files are ignored as long as .log files are present. By default
  each file extension recognized is linked to a parsing subroutine (cf. above).
  When the script is called without command line arguments, the user is asked
  to enter the method of charge analysis manually (except *.xyz where no charge
  information is present, notations like [UC/lc] give UC on pressing return).
  
  When mobcal.exe is found in the working directory, the program is executed
  automatically. When finished, the MD5 checksum of mobcal.exe, as
  well as the mfj and run files are appended to the output file (*.mob).
  The MD5 checksum could later on be used to identify the MOBCAL build used
  to calculate the CCS and mobilities.
  
  In the end, a new directory is created where both the input (*.log or else)
  and the output (*.mob) are moved.

== MULTI-GEOMETRY OUTPUT ======================================================

  Multiple files with one of the specified file extensions are treated as
  ISOMERS and appended to the same MOBCAL file. MOBCAL in turn uses this type
  of input to average the CCS of different isomers (rotamers). When converting
  multiple files, be sure not to accidently have files of the same file
  extension present in your working directory, as all files will be appended
  to the same hashes.

  Either rename or delete the files or use command line switches (scroll down).
  If the default settings are not suitable for your purposes, which could be
  the case if e.g. your gaussian files have a different file extension than
  *.log (e.g. *.g09) you may want to use command line switches (scroll down)
  or modify config.cfg.

== CONFIGURATION FILE config.cfg ==============================================

  When the program is started for the first time, this text is displayed and
  the user is asked, whether or not a new config.cfg file should be created.
  This status can be reset by deleting or renaming the config.cfg file in the
  working directory.

  MOBCAL recognizes different elements by their integer mass. However, by
  default MOBCAL uses the same parameters as for silicon for heavier elements.
  Each element that is found in your geometry file (ORCA, GAUSSIAN or else)
  has to be specified in the element table present in config.cfg. However,
  the integer mass you enter has to be present in MOBCAL source code, if it is
  not you can use a workaround (cf. config.cfg & MOBCAL code LINE 577 ff).

  You can also change the default file extensions used for automatic
  processing by changing the flag in line 4.
  
  Colored ANSI output can be enabled by setting the flag in line 6, this
  is not compatible to cmd.exe (Win32) by default. Jason Hood's ANSICON is
  capable of displaying ANSI escapes in Win32 (adoxa.110mb.com/ansicon/),
  which works with TERM::ANSIcolor package under Win32. It greatly improves
  the readability of the screen output, so it's worth the effort.

== Protein Database Format (pdb) ==============================================

  A rudimentary support for *.pdb file parsing has been implemented in the
  beta release. However, this routine does not support actual protein database
  files. The support is limited to simple *.pdb files generated by certain
  molecular modelling software (e.g. Avogadro).

== COMMAND LINE SWITCHES ======================================================

  SWITCHES OVERRIDE MOST OF THE FULLY AUTOMATIC PROCESSING ROUTINES. THE
  PASS THROUGH TO MOBCAL IS DISABLED TO ENABLE EXTERNAL ACCESS BY SCRIPTS.

-- 1st EXAMPLE ----------------------------------------------------------------

  mobcalPARSER.pl cmd g09 gauss

  Calls the script to search for *.g09 files and parse them using the
  Gaussian routine (ORCA subroutine is called with 'orca'). The automatic
  file search routine is enabled when the cmd switch is used.

-- 2nd EXAMPLE ----------------------------------------------------------------

  mobcalPARSER.pl noav example.g03 gauss mulliken

  'noav' overrides automatic filesearch. The following switches call the script
  to parse the specified file (example.g03) with gaussian subroutine (gauss)
  using Mulliken charges (alternatively 'none' would override the
  charge analysis). noav overrides ALL automatic routines. The filename
  specified in line 2 of config.cfg contains the mobcal compatible input (mfj).

== Artistic License ===========================================================

  This program comes with absolutely no warranty, the source code is licensed
  under the "Artistic License". This license is part of the source code
  and is displayed when the program is started for the first time by default.
  Type "mobcalPARSER.pl c" to view the license. This software comes with
  ABSOLUTELY NO WARRANTY.
  
== KNOWN ISSUES (PLASE ADD YOUR COMMENTS) =====================================

 <!> Special characters in file names are not displayed properly
 <!> Only three character file extensions are compatible
 <!> Linux compatibility untested

===============================================================================
============================  J.P. Boyd Jul 2011 ==============================
===============================================================================
CMDNOTES
); $kill=<STDIN>}
START:
if (-e 'config.cfg') {
  open (CONFIG,"config.cfg");
  @CONFIG=<CONFIG>;
  close (CONFIG);
  $mobcalexec=@CONFIG[7];
  chomp($mobcalexec);
  $ANSI=@CONFIG[5];
  $outputfilename= $CONFIG[1];
  chomp($outputfilename);
  $fileextension= reverse(substr($CONFIG[3],0,3));
  if ($ANSI=~"yes"){
    use Term::ANSIColor;
    $dash= colored ("===============================================================================", 'cyan')."\n";
    $reddash= colored ("===============================================================================", 'white on_red')."\n";
    $warning= colored ("\n==WARNING:=====================================================================\a\a\a", 'white on_red')."\n";
    $note= colored ("\n==NOTE:========================================================================", 'cyan')."\n";
    $timefiller=colored ("\n==READ WHILE WAITING:==========================================================\n", 'green');
    $failed= colored("FAILED", 'red');
    print color 'cyan';
  }
print <<LOGO
===============================================================================
===============================================================================
              =======  =======  =======  ======  ======== =======
              ===  === ===  === ===  === ===     ===      ===  ===
              =======  ======== =======   =====  ======   =======
              ===      ===  === === ===      === ===      === ===
              ===      ===  === ===  === ======  ======== ===  ===
===============================================================================
===============================================================================
LOGO
;
if ($ANSI=~"yes"){print color 'reset'};
if (not $ARGV[0] =~ "help"){
  print "  Type 'mobcalPARSER.pl c' for license.\n";
  print "  Type 'mobcalPARSER.pl h' for more information.\n";
};
} else {
  print $note;
  print "  NO config.cfg FILE FOUND IN WORKING DIRECTORY. GENERATE [YES/no]? ";
  $kill=<STDIN>;
  print $dash;
  if (not $kill=~"no"){
    open (CONFIG,">config.cfg");
################################################################################
(print CONFIG <<CONFIGTEMPLATE
#Output filename:
MOBCAL.mfj
#Default file extensions (orca<SPACE>gaussian):
out log
#Use ANSI Color [NO/yes]?
NO
#MOBCAL EXECUTABLE COMMAND (change to "./mobcal" under linux):
mobcal.exe
# The following table contains a selection of integer masses
# assigned to various element symbols. Lots of Elements are
# replaced by silicon (28). The reason is found in MOBCAL source
# code (fortran77) starting at line 577. You may add additional
# elements in the format provided below. However, providing the
# actual integer masses (e.g. 'Ar 40') requires modification of
# the original MOBCAL source code and is quite useless, as long
# as no suitable parameters are known.
Integer masses of atoms:
H   1
C  12
N  14
O  16
Na 23
Si 28
S  32
Fe 56
B  12
F  16
Cl 28
Br 28
I  28
P  28
Sc 28
Ti 28
V  28
Cr 28
Mn 28
Co 28
Ni 28
Cu 28
Zn 28
CONFIGTEMPLATE
); close(CONFIG);
goto START;} else {goto KILL2}
};
################################################################################
print $dash;
print "  LOOKING FOR *.".reverse($fileextension)." FILES (ORCA)...\n";
if ($ARGV[0] =~ 'cmd'){
  $fileextension=reverse($ARGV[1])
}
FILESEARCH: @files = <*>;
@chom= @files; $geomcounter= -1; $filecounter= 0;
if (($#ARGV== -1) or $ARGV[0] =~ "cmd"){
  @files = <*>; @chom= @files; $geomcounter= -1; $filecounter= 0;
  foreach (@chom) {
    $_= reverse($_); $_= substr($_,0,3);
    $filecounter++;
    if ($_=~ "$fileextension") {
      $geomcounter++;
      @filenames[$geomcounter]= @files[$filecounter-1];
    }
  }
  $geometries= $geomcounter+1;
}
if ($ARGV[0] =~ "noav"){
  @filenames=();
  @filenames[0]=$ARGV[1];
  $geometries=1;
  $chargeanalysis= $ARGV[3];
  $chargeanalysis= uc($chargeanalysis);
  $fileextension="n\/a";
  print $dash;
  print "================== AUTOMATIC FILE SELECTION OVERRIDE ENABLED ===================\n";
  print $dash;
}
if (($#ARGV == -1) and ($geomcounter== -1) and $fileextension=~reverse(substr($CONFIG[3],0,3))){
  $fileextension=reverse(substr($CONFIG[3],4,3));
  print "  ".$failed.", LOOKING FOR *.". substr($CONFIG[3],4,3) ." FILES (GAUSSIAN)...\n";
  goto FILESEARCH;
}
if (($#ARGV == -1) and ($geomcounter== -1) and $fileextension=~reverse(substr($CONFIG[3],4,3))){
  $fileextension="zyx";
  print "  ".$failed.", LOOKING FOR *.xyz FILES... \n";
  goto FILESEARCH;
}
if (($#ARGV == -1) and ($geomcounter== -1) and $fileextension=~"zyx"){
  $fileextension="lom";
  print "  ".$failed.", LOOKING FOR *.mol FILES... \n";
  goto FILESEARCH;
}
if (($#ARGV == -1) and ($geomcounter== -1) and $fileextension=~"lom"){
  $fileextension="bdp";
  print "  ".$failed.", LOOKING FOR *.pdb FILES (purely experimental)... \n";
  goto FILESEARCH;
}
if (($#ARGV == -1) and ($geomcounter== -1) and ($fileextension=~"bdp")){
  print "  NO SUITABLE FILES FOUND. TYPE 'mobcalPARSER.pl h' FOR MORE INFORMATION.";
  goto KILL;
}
if (($#ARGV == -1) or $ARGV[0]=~"cmd"){
  print $dash;
  print "  FILE(S) SELECTED FOR AUTOMATIC PROCESSING:\n";
  print $dash;
  foreach $file (@files) {
    foreach (@filenames){
      if ($_=~$file){
       print "  $file\n"
      }
    }
  }
}
print $dash;
if ($geometries>1){
  print $note;
  print "  $geometries Geometries will be treated as ISOMERS of the same species.\n";
  print "  There is an error routine present, which allows writing to disk only if\n";
  print "  the files indeed contain isomeric geometry data. If you get a WARNING,\n";
  print "  rename all but one file from *." . reverse($fileextension) . " to";
  print " *." . reverse($fileextension) . "_ and restart the program or\n";
  print "  use command line option 'noav'.\n";
  print $dash;
};
  if (($chargeanalysis =~ "LOEWDIN") and ($ARGV[2]=~"gauss")){
    print $note;
    print "  LOEWDIN CHARGE ANALYSIS IS NOT PRESENT IN STANDARD GAUSSIAN\n";
    print "  OUTPUT, THE COMMAND COMBINATION YOU ENTERED IS NOT SUPPORTED.\n";
    goto KILL2;
  }

######################## PARSER SUBROUTINES ####################################

################################################################################
########################## ORCA SUBROUTINE #####################################
################################################################################
if ($fileextension=~"tuo" or $ARGV[2] =~ "orca"){
  if (($#ARGV == -1) or ($ARGV[0] =~ "cmd")){
    print "  SELECT CHARGE ANALYSIS: [MULLIKEN/loewdin/none]: ";
    $chargeanalysis= <STDIN>;
    print $dash;
    if ((not $chargeanalysis=~"loewdin")&(not $chargeanalysis=~"none")) {
      $chargeanalysis= "MULLIKEN"
    }
    $chargeanalysis= uc($chargeanalysis);
  }
  foreach $inputfilename (@filenames){
      print "\n".$note;
      print "  PROCESSING $inputfilename\n";
      print $dash;
      open(INPUT,$inputfilename); @array= <INPUT>; close (INPUT);
      $counter= 0; $optstart= 0; $chargestart= 0;
      foreach $line (@array){
          $counter ++;
          if ($line =~"FINAL ENERGY EVALUATION AT THE STATIONARY POINT"){
              $optstart = $counter+5}
          if ($line =~"CARTESIAN COORDINATES"){
              $optend = $counter-4}
          if (not ($chargeanalysis=~ "loewdin")){
            if ($line =~"MULLIKEN ATOMIC CHARGES AND SPIN POPULATIONS"){
              $chargestart = $counter+1}
            if ($line=~"MULLIKEN REDUCED ORBITAL CHARGES AND SPIN POPULATIONS"){
              $chargeend = $counter-6}
          }
          if ($chargeanalysis=~ "loewdin"){
            if ($line=~"LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS"){
              $chargestart = $counter+1}
            if ($line =~"LOEWDIN REDUCED ORBITAL CHARGES AND SPIN POPULATIONS"){
              $chargeend = $counter-4}
          }
      }
  if (not $optstart == 0){
    print "\nFINAL CARTESIAN COORDINATES (ANGSTROMS) FOUND IN LINES $optstart TO $optend\n";
    @index1= ($optstart .. $optend); @geom= @array[@index1];
  }
  else {
    print $note;
    print "  NO GEOMETRY OPTIMIZATION FOUND (ORCA), LOOKING FOR INITIAL COORDINATES...\n";
    $counter= 0;
    foreach $line (@array){
      $counter ++;
      if ($line =~ "Single Point Calculation"){$optstart = $counter+5;};
      if ($line =~ "CARTESIAN COORDINATES"){$optend = $counter-4;};
    }
    @index1= ($optstart .. $optend); @geom= @array[@index1];
    if (not $optstart == 0){
      print "  INITIAL COORDINATES (ANGSTROMS)FOUND IN LINES $optstart TO $optend\n";
      print $dash
    }
  }
  if ($optstart == 0){
    print "  FILE RECOGNITION ERROR, NO VALID ORCA GEOMETRY FOUND (cf. config.cfg).\n";
    print $dash;
    goto KILL2;
  }
  @label= @geom;
  foreach (@label){$_=substr($_,2,2)}
  print "\nELEMENTS ADDED TO HASH\n";
  foreach (@label){print "  " . $_ . "      " };
  @{$labelhash{$inputfilename}}= @label;
  @x= @geom; @y= @geom; @z= @geom;
  foreach (@x){$_=substr($_,6,11);}
  foreach (@y){$_=substr($_,18,11);}
  foreach (@z){$_=substr($_,30,11);}
  @{$xhash{$inputfilename}}= @x;
  @{$yhash{$inputfilename}}= @y;
  @{$zhash{$inputfilename}}= @z;
  print "\n\nX-VALUE ADDED TO HASH\n";
  foreach (@{$xhash{$inputfilename}}){print substr($_,1,10)}
  print "\n\nY-VALUE ADDED TO HASH\n";
  foreach (@{$yhash{$inputfilename}}){print substr($_,1,10)}
  print "\n\nZ-VALUE ADDED TO HASH\n";
  foreach (@{$zhash{$inputfilename}}){print substr($_,1,10)}
  @index2= ($chargestart .. $chargeend);
  @charges= @array[@index2];
  foreach (@charges){$_=substr($_,10,10);}
  if ((not $chargestart == 0) & ($chargeanalysis=~ "MULLIKEN")){
    print
    "\n\nMULLIKEN CHARGES FOUND IN LINES $chargestart TO $chargeend ADDED TO HASH\n";
    $filelength= 0;
    @{$chargehash{$inputfilename}}= @charges;
    foreach (@{$chargehash{$inputfilename}}){
      print $_; $filelength++;
    }
  }
  if ((not $chargestart == 0) & ($chargeanalysis=~ "LOEWDIN")){
    print
    "\n\nLOEWDIN CHARGES FOUND IN LINES $chargestart TO $chargeend ADDED TO HASH\n\n";
    $filelength= 0; @{$chargehash{$inputfilename}}= @charges;
    foreach (@{$chargehash{$inputfilename}}){
      print $_; $filelength++;
    }
  }
  if ($chargeanalysis=~ "NONE"){
      print
      "\n\nOVERRIDING POPULATION ANALYSIS, SETTING ALL CHARGES TO 0.00000\n\n";
      $filelength= 0;
      @{$chargehash{$inputfilename}}= @charges;
      foreach (@{$chargehash{$inputfilename}}){$_= "  0.00000"; $filelength++;}
  }
}
print "\n";
print $note;
print "  ORCA SUBROUTINE DONE\n";
print $dash;
@index= (0 .. ($chargeend - $chargestart)); goto INTERFACING;
}
################################################################################
######################## GAUSSIAN SUBROUTINE ###################################
################################################################################
if ($fileextension=~"gol" or $ARGV[2]=~ "gauss"){
  if (($#ARGV == -1) or ($ARGV[0] =~ "cmd")){
    print "  SELECT CHARGE ANALYSIS: [MULLIKEN/none]: ";
    $chargeanalysis= "MULLIKEN";
    print $dash;
    if (not $chargeanalysis=~"none"){$chargeanalysis= "MULLIKEN"};
    $chargeanalysis= uc($chargeanalysis);
  }
  foreach $inputfilename (@filenames){
      print $note;
      print "  PROCESSING $inputfilename\n";
      print $dash;
      open(INPUT,$inputfilename); @array= <INPUT>; close (INPUT);
      $hurray=0;
      OVERRIDE:
      $versionline=0;
      $optstart= 0;
      $chargestart= 0;
      $chargeend=0;
      $counter=0;
      foreach (@array){
          $counter++;
          if (($_=~"Cite this work as") and ($versionline == 0)){
            $versionline=$counter;
          }
          if (($_ =~ "Optimization completed") and ($hurray == 0)){
            $hurray=$counter
          }
          if (($_ =~ "Standard orientation")
          and (not $hurray == 0)
          and ($optstart == 0)){
             $optstart = $counter+4
          }
          if ((($_=~"Mulliken atomic charges")
            or ($_=~"Total atomic charges"))
          and (not $hurray == 0)
          and ($chargestart == 0)){
             $chargestart = $counter+1
          }
          if ((($_ =~ "Mulliken charges with hydrogens")
            or ($_ =~ "Atomic charges with hydrogens"))
           and (not $hurray == 0) and $chargeend == 0){
            $chargeend=$counter-3
          }
      }
      if ($hurray==0){
        print $warning;
        print "  NO OPTIMIZATION FOUND.";
        if ($#ARGV==-1){
          print " WOULD YOU LIKE TO CONTINUE ANYWAY (NO/yes)?";
          $kill=<STDIN>;
          if ($kill=~"yes"){
#            $chargeanalysis="NONE";
            $hurray=1;
            print $reddash;
            goto OVERRIDE;
          } else {print $reddash; goto KILL2}
        } else {print "\n"; print $reddash; goto KILL2};
          print $reddash;
      }
      $gaussianversion= @array[$versionline];
      $gaussianversion= substr($gaussianversion,0,12);
      if ($ANSI=~yes){
        print colored ("  MAYOR RELEASE: $gaussianversion\n", 'yellow');
        print $dash."\n";
      } else {
        print "  MAYOR RELEASE: $gaussianversion\n";
        print $dash."\n";
      }
      $optend=$optstart+$chargeend-$chargestart;
      print "FINAL CARTESIAN COORDINATES (ANGSTROMS) FOUND IN LINES ".($optstart)." TO ".($optend)."\n";
      @index1= ($optstart .. $optend);
      @index2= ($chargestart .. $chargeend);
      @geom= @array[@index1];
      @charges= @array[@index2];
      @label= @charges;
############################################################################
      if (not $gaussianversion=~"Gaussian 9"){
        foreach (@label){$_=substr($_,8,2)}
      } else {
        foreach (@label){$_=substr($_,5,2)}
      }
############################################################################
      print "\nELEMENTS ADDED TO HASH:\n";
      foreach (@label){print "  " . $_ . "      " };
      @{$labelhash{$inputfilename}}= @label;
      @x= @geom; @y= @geom; @z= @geom;
      if (not $gaussianversion=~"Gaussian 94"){
         foreach (@x){$_=substr($_,35,11)}
         foreach (@y){$_=substr($_,47,11)}
         foreach (@z){$_=substr($_,59,11)}
      }
      else {
         foreach (@x){$_=substr($_,24,11)}
         foreach (@y){$_=substr($_,36,11)}
         foreach (@z){$_=substr($_,48,11)}
      }
      @{$xhash{$inputfilename}}= @x;
      @{$yhash{$inputfilename}}= @y;
      @{$zhash{$inputfilename}}= @z;
      print "\n\nX-VALUE ADDED TO HASH\n";
      foreach (@{$xhash{$inputfilename}}){print substr($_,1,10)}
      print "\n\nY-VALUE ADDED TO HASH\n";
      foreach (@{$yhash{$inputfilename}}){print substr($_,1,10)}
      print "\n\nZ-VALUE ADDED TO HASH\n";
      foreach (@{$zhash{$inputfilename}}){print substr($_,1,10)}
############################################################################
      if ($gaussianversion=~"Gaussian 0"){
        foreach (@charges){$_=substr($_,11,10)
        }
      } else {
        foreach (@charges){$_=substr($_,8,10)}
      }
############################################################################
      
  if ((not $chargestart == 0) & ($chargeanalysis=~ "MULLIKEN")){
      print
      "\n\nMULLIKEN CHARGES FOUND IN LINES $chargestart TO $chargeend ADDED TO HASH\n";
      $filelength= 0;
      @{$chargehash{$inputfilename}}= @charges;
      foreach (@{$chargehash{$inputfilename}}){
        print $_;
        $filelength++;
      };
  } else {
      print
      "\n\nOVERRIDING POPULATION ANALYSIS, SETTING ALL CHARGES TO 0.00000\n";
      $filelength= 0;
      @{$chargehash{$inputfilename}}= @charges;
      foreach (@{$chargehash{$inputfilename}}){$_= "  0.00000"; $filelength++}
  }
  if ($#ARGV==-1){
    $wisenheimerstart=$#array;
    $wisenheimerend=$wisenheimerstart;
    while (not @array[$wisenheimerstart]=~ "@"){
      $wisenheimerstart--;
    }
    while (not @array[$wisenheimerend]=~ "Job"){
      $wisenheimerend--;
    }
    @wisenheimerindex= $wisenheimerstart+2 .. $wisenheimerend-1;
    print "\n";
    print $timefiller;
    if ($ANSI=~"yes"){print color 'green'};
    foreach (@wisenheimerindex) {
      print " ".@array[$_];
    }
    if ($ANSI=~"yes"){print color 'reset'};
}
}
print $note;
print "  GAUSSIAN SUBROUTINE DONE \n";
print $dash;
@index= (0 .. ($chargeend - $chargestart)); goto INTERFACING;
}
################################################################################
############################# XYZ Subroutine ###################################
################################################################################
if ($fileextension=~ "zyx" or $ARGV[2]=~ "xyz"){
  $chargeanalysis="NONE";
  foreach $inputfilename (@filenames){
      print "\n";
      print $note;
      print "  PROCESSING $inputfilename\n";
      print $dash;
      open(INPUT,$inputfilename); @array= <INPUT>; close (INPUT);
      $counter= 0;
      foreach $line (@array){$counter ++;}
      $filelength= $counter-2;
      shift(@array);
      if (substr(@array[0],0,14)=~"XYZ file for :"){
          $xyzversion='ortep'
      }
      else {$xyzversion='avogadro'}
      shift(@array); @label= @array;
      if ($xyzversion=~'ortep'){
        foreach (@label){$_=substr($_,1,2)};
        foreach (@label){
            if (substr($_,0,1)=~" "){
              $_=substr($_,1,1)." "
            }
        }
      }
      else {foreach (@label){$_=substr($_,0,2)}}
      @{$labelhash{$inputfilename}}= @label;
      print "\nELEMENTS ADDED TO HASH:\n";
      foreach (@{$labelhash{$inputfilename}}){print "  " . $_ . "      " }
      @x= @array; @y= @array; @z= @array;
      foreach (@x){$_=substr($_,8,10)}
      foreach (@y){$_=substr($_,23,10)}
      foreach (@z){$_=substr($_,38,10)}
      @{$xhash{$inputfilename}}= @x; print "\n\nX-VALUE ADDED TO HASH\n";
      foreach (@{$xhash{$inputfilename}}){print substr($_,0,10)}
      @{$yhash{$inputfilename}}= @y; print "\n\nY-VALUE ADDED TO HASH\n";
      foreach (@{$yhash{$inputfilename}}){print substr($_,0,10)}
      @{$zhash{$inputfilename}}= @z; print "\n\nZ-VALUE ADDED TO HASH\n";
      foreach (@{$zhash{$inputfilename}}){print substr($_,0,10)}
      @{$chargehash{$inputfilename}}= @label;
      foreach (@{$chargehash{$inputfilename}}){$_= "  0.000000"}
  }
print "\n";
print $note;
print "  XYZ SUBROUTINE DONE \n";
print $dash;
@index= (0 .. ($filelength-1)); goto INTERFACING;
}
################################################################################
############################### mol Subroutine #################################
################################################################################
if ($fileextension=~ "lom" or $ARGV[2]=~ "mol"){
  $chargeanalysis="NONE";
  foreach $inputfilename (@filenames){
      print "\n";
      print $note;
      print "  PROCESSING $inputfilename\n";
      print $dash;
      open(INPUT,$inputfilename);
      @array= <INPUT>;
      close (INPUT);
      if (substr(@array[3],0,2) =~"  "){$filelength= substr(@array[3],2,1)}
      elsif (substr(@array[3],0,1) =~" "){$filelength= substr(@array[3],1,2)}
      else {$filelength= substr(@array[3],0,3)};
      @index3= 0 .. $filelength-1;
      foreach (@index3) {
        $label[$_]=substr($array[$_+4],31,2);
        $x[$_]=substr($array[$_+4],1,9);
        $y[$_]=substr($array[$_+4],11,9);
        $z[$_]=substr($array[$_+4],21,9);
      }
      @{$labelhash{$inputfilename}}= @label; print "\nELEMENTS ADDED TO HASH:\n";
      foreach (@{$labelhash{$inputfilename}}){print "  " . $_ . "      " }
      @{$xhash{$inputfilename}}= @x; print "\n\nX-VALUE ADDED TO HASH\n";
      foreach (@{$xhash{$inputfilename}}){print substr($_,1,10)}
      @{$yhash{$inputfilename}}= @y; print "\n\nY-VALUE ADDED TO HASH\n";
      foreach (@{$yhash{$inputfilename}}){print substr($_,1,10)}
      @{$zhash{$inputfilename}}= @z; print "\n\nZ-VALUE ADDED TO HASH\n";
      foreach (@{$zhash{$inputfilename}}){print substr($_,1,10)}
      @{$chargehash{$inputfilename}}= @label;
      foreach (@{$chargehash{$inputfilename}}){$_= "  0.000000"}
  }
print "\n";
print $note;
print "  mol SUBROUTINE DONE \n";
print $dash;
@index= (0 .. ($filelength-1)); goto INTERFACING;
}
################################################################################
######################### Experimental pdb Subroutine ##########################
################################################################################
if ($fileextension=~ "bdp" or $ARGV[2]=~ "pdb"){
  $chargeanalysis="NONE";
  foreach $inputfilename (@filenames){
      print "\n";
      print $note;
      print "  PROCESSING $inputfilename\n";
      print $dash;
      open(INPUT,$inputfilename);
      @array= <INPUT>;
      close (INPUT);
################################################################################
      if (not substr(@array[2],0,6)=~"HETATM"){
          print $warning;
          print "  THIS FEATURE OF THE PROGRAM IS STILL IN DEVELOPMENT. THE FILE APPEARS TO\n";
          print "  BE TOO COMPLEX FOR THE PRESENTLY IMPLEMENTED PDB PARSER ROUTINE (v0.0.1).\n";
          print $reddash;
          goto KILL2;
      }
################################################################################
      while (not $array[0] =~ "HETATM"){
        shift @array;
      }
      while (not $array[$#array] =~ "HETATM"){
        pop @array;
      }
      $filelength= $#array+1;
      @label= @array;
      foreach (@label){$_=substr($_,13,2)};
      @{$labelhash{$inputfilename}}= @label;
      print "\nELEMENTS ADDED TO HASH:\n";
      foreach (@{$labelhash{$inputfilename}}){print "  " . $_ . "      " }
      @x= @array; @y= @array; @z= @array;
      foreach (@x){$_=substr($_,30,8)}
      foreach (@y){$_=substr($_,38,8)}
      foreach (@z){$_=substr($_,46,8)}
      @{$xhash{$inputfilename}}= @x; print "\n\nX-VALUE ADDED TO HASH\n";
      foreach (@{$xhash{$inputfilename}}){print $_}
      @{$yhash{$inputfilename}}= @y; print "\n\nY-VALUE ADDED TO HASH\n";
      foreach (@{$yhash{$inputfilename}}){print $_}
      @{$zhash{$inputfilename}}= @z; print "\n\nZ-VALUE ADDED TO HASH\n";
      foreach (@{$zhash{$inputfilename}}){print $_}
      @{$chargehash{$inputfilename}}= @label;
      foreach (@{$chargehash{$inputfilename}}){$_= "  0.00000"}
  }
print "\n";
print $note;
print "  PDB SUBROUTINE DONE \n";
print $dash;
@index= (0 .. ($filelength-1)); goto INTERFACING;
}
################################################################################
########################## Interface Subroutine ################################
################################################################################
INTERFACING:
while (not $CONFIG[0] =~ "Integer masses of atoms:"){
  shift(@CONFIG)
}
shift(@CONFIG);
$elementcounter= 0;
$labelalert=0;
foreach $ELEMENT (@CONFIG) {
    foreach $inputfilename (@filenames){
      foreach (@{$labelhash{$inputfilename}}){
        if ($_ =~ substr($ELEMENT,0,2)){
            $_=substr($ELEMENT,3,2);
            $elementcounter++;
        ### calculating sum formula using hash###
            $elementkey= substr($ELEMENT,0,2);
            if (substr($elementkey,1,1)=~" "){
               $elementkey=substr($elementkey,0,1)
            }
            if (not exists $sumformulahash{$elementkey}){
              ($sumformulahash{$elementkey}=1)
            }
            else {($sumformulahash{$elementkey})++}
        ### setting labelalert flag ###
            if ((substr($ELEMENT,3,2)=~ "28")
                and (not substr($ELEMENT,0,2)=~"Si")) {
                $labelalert=1;
            }
            if ((substr($ELEMENT,3,2)=~ "12")
                and (not substr($ELEMENT,0,2)=~"C")) {
                $labelalert=1;
            }
            if ((substr($ELEMENT,3,2)=~ "16")
                and (not substr($ELEMENT,0,2)=~"O ")) {
                $labelalert=1;
            }
        }
      }
    }
}
#print $note;
#foreach $inputfilename (@filenames){
#  print "\nINTEGERS REPLACING ELEMENT SYMBOLS IN <" . $inputfilename . ">\n";
#  foreach (@{$labelhash{$inputfilename}}){
#    print "  " . $_ . "      ";
#  }
#  print "\n\n";
#}
if ($labelalert==1) {
  print $note;
  print "  MOBCAL PARAMETERS FOR SOME ELEMENTS IN YOUR GEOMETRY ARE LACKING, INTEGER\n";
  print "  MASS IS SET TO CLOSEST VALUE AVAILABLE (cf. config.cfg & MOBCAL source code).\n";
  print $dash;
}
if ((($elementcounter / $geometries) != $filelength) and ($geometries == 1)){
  print $warning;
  print "  YOUR config.cfg FILE SEEMS TO LACK SOME NECESSARY ELEMENT DEFINITIONS,\n";
  print "  CERTAIN ELEMENT SYMBOLS ARE NOT REPLACEABLE BY INTEGER MASSES (cf. above).\n";
  print $reddash;
  goto KILL2;
}
if ((($elementcounter / $geometries) != $filelength) and ($geometries > 1)){
  print $warning;
  print "  EITHER YOUR config.cfg FILE LACKS SOME NECESSARY ELEMENT DEFINITIONS OR THE\n";
  print "  GEOMETRIES PRESENT IN THE FILES YOU PROVIDED ARE NOT ISOMERIC (cf. above).\n";
  print $reddash;
  goto KILL2;
}
### sorting sumformula and generating filename from sumformula ###
$sumformula="";
$mobcaloutput="";
if (exists $sumformulahash{"C"}){
  $sumformula= $sumformula ."C".$sumformulahash{"C"}/$geometries;
  delete $sumformulahash{"C"}
}
if (exists $sumformulahash{"H"}){
  $sumformula= $sumformula . "H".$sumformulahash{"H"}/$geometries;
  delete $sumformulahash{"H"}
}
foreach $elementkey (sort(keys(%sumformulahash))){
  $sumformula= $sumformula . $elementkey . $sumformulahash{$elementkey}/$geometries;
}
$mobcaloutput=$sumformula. ".mob";
### sorting done ###
$timechop=scalar(localtime);
$timechop= substr($timechop,8,2).substr($timechop,4,3).substr($timechop,length($timechop)-2,2)." ".substr($timechop,11,5);
$title= $sumformula . " - " . $timechop;

foreach $inputfilename (@filenames){
	(my $without_extension = $inputfilename) =~ s/\.[^.]+$//;
@OUTPUT[0]="$title\n";
@OUTPUT[1]="$geometries\n";
@OUTPUT[2]="$filelength\n";
@OUTPUT[3]="ang\n";
@OUTPUT[4]="calc\n";
if ($chargeanalysis =~ "NONE"){@OUTPUT[4]="none\n";}
@OUTPUT[5]="1.0000";
$linecounter= 0;
$header= 6;

  foreach $index (@index){
    @OUTPUT[$index + $header]=
    "\n\t$xhash{$inputfilename}[$index]".
    "\t$yhash{$inputfilename}[$index]".
    "\t$zhash{$inputfilename}[$index]".
    "\t$labelhash{$inputfilename}[$index]".
    "\t$chargehash{$inputfilename}[$index]";
    $linecounter++;
  }
  $header= ($linecounter+$header);
  @OUTPUT[$header]= "\n$filelength";
  $header++;
open (OUTPUT,">$without_extension" . '.mfj');
print OUTPUT @OUTPUT;
close OUTPUT;
### Generating mobcal.run file ###
  @MOBCALRUN[0]= "$without_extension".'.mfj'."\n";
  @MOBCALRUN[1]= "$without_extension".'.mob'."\n";
  @MOBCALRUN[2]= substr(rand(8999999),0,7)+1000000 . "\n";
  open (MOBCALRUN,">$without_extension" . '.run');
  print MOBCALRUN @MOBCALRUN;
  close MOBCALRUN;
}
print "  $geometries GEOMETRY(IES) PROCESSED, $outputfilename CONTAINS MOBCAL INPUT.\n";

### AUTOMATIC MOBCAL EXECUTION ###
if (($#ARGV==-1) and ($^O=~"Win")){
  if (-e $mobcalexec){
    $md5 = Digest::MD5->new;
    open(MD5check, $mobcalexec) or die "  Error: Could not open for MD5 checksum";
    binmode(MD5check);
    $md5sum = $md5->addfile(*MD5check)->hexdigest;
    close MD5check;
    print "  RUNNING MOBCAL, PLEASE WAIT... ";
    system($mobcalexec);
  } else {
    print "\n  COULD NOT FIND $mobcalexec IN WORKING DIRECTORY, PLEASE COMPILE\a\a\a\n";
    print "  FROM SOURCE AND RESTART THE FRONTEND"; goto KILL2
    }
  print "CALCULATION COMPLETE\a\n";
  open (MOBCALRESULTS,$mobcaloutput);
    @mobcalresults=<MOBCALRESULTS>;
  close MOBCALRESULTS;
  open (MOBCALRESULTS,">>$mobcaloutput");
    print MOBCALRESULTS "\nPARSER COMMENTS\nMD5(mobcal.exe) = ".$md5sum;
    if (not $chargeanalysis=~"NONE"){print MOBCALRESULTS "\n\ncharges:\n$chargeanalysis"};
    print MOBCALRESULTS "\n.mfj generated from file(s):\n";
    foreach (@filenames){print MOBCALRESULTS "$_\n"};
    print MOBCALRESULTS "\nCOPY OF MFJ INPUT:\n";
    print MOBCALRESULTS @OUTPUT;
    print MOBCALRESULTS "\n\nUSING SEED INTEGER:\n";
    print MOBCALRESULTS @MOBCALRUN;
    print MOBCALRESULTS "\nEND OF FILE - ".scalar(localtime);
  close MOBCALRESULTS;
  $summaryfound=0;
  foreach (@mobcalresults) {
    if ($_=~"SUMMARY"){
     $summaryfound=1
    }
  }
  if ($summaryfound==1){
    while (not $mobcalresults[0]=~ "SUMMARY"){
      shift @mobcalresults
    }
  } else {print "  MOBCAL ENCOUNTERED ERRORS\n"; $dirname="MOBCAL_ERROR"; goto SAFETYCHECK2}
  print $dash;
  print "  SUMMARY FOR MOBCAL OUTPUT ".$mobcaloutput."\n";
  print $dash;
  if ($ANSI=~yes){print color 'yellow'}; print "\n";
  if (not $geometries>1){
    foreach (@mobcalresults){
     if ($_=~"MOBIL"){
       print "\n"
     }
     if (($_=~"temperature") or ($_=~"label") or ($_=~"cross") or ($_=~"deviation") or ($_=~"mobility")){
      chomp $_;
      print " ".$_."\n"
     }
    }
  } else {
          foreach (@mobcalresults){
        if ($_=~"MOBIL"){
          print "\n";
        }
        if (($_=~"temperature") or ($_=~"MOBIL") or ($_=~"AVGE") or ($_=~"set")){
          chomp $_;
          print " ".$_."\n"
        }
      }
  }
  if ($ANSI=~yes){print color 'reset'};
  $dirname=substr($timechop,5,2).substr($timechop,2,3).substr($timechop,0,2)."_".substr($mobcaloutput,0,length($mobcaloutput)-4);
  SAFETYCHECK2:
  if (-d $dirname){
    $dirname=$dirname."_".substr((rand(899)+100),0,3);
    goto SAFETYCHECK2;
  }
  mkdir $dirname;
  move($mobcaloutput,$dirname);
  unlink($outputfilename);
  unlink("mobcal.run");
  foreach (@filenames){
    move($_,$dirname)
  }
  if ($dirname=~"MOBCAL_ERROR"){goto KILL2};
}
KILL:
print "\n" . $dash;
print "  NORMAL TERMINATION OF PROCESS $$ ON ". scalar(localtime). " AT $^O\n";
print $dash;
goto KILL3;
KILL2:
print "\n" . $reddash;
print "  ERROR TERMINATION OF PROCESS $$ ON ". scalar(localtime). " AT $^O\a\a\n";
print $reddash;
KILL3:

