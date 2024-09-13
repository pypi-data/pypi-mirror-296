import argparse
import sys
import os
from chrori.__init__ import __version__

class Params(object):

    def __init__(self, program_name):
        self.program_name = program_name

    def set_options(self):
        if self.program_name == 'mkvcf':
            parser = self.mkvcf_options()
        elif self.program_name == 'select':
            parser = self.select_options()
        elif self.program_name == 'visual':
            parser = self.visual_options()

        if len(sys.argv) == 1:
            args = parser.parse_args(['-h'])
        else:
            args = parser.parse_args()
        return args
    
    def mkvcf_options(self):
        parser = argparse.ArgumentParser(description='chrori version {}'.format(__version__),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('chrori_mkvcf -r <FASTA> -b <BAM_1> -b <BAM_2>... -n <name_1> -n <name_2>... -O <STRING>\n')

        # set options
        parser.add_argument('-r', '--ref',
                            action='store',
                            required=True,
                            type=str,
                            help='Reference fasta.',
                            metavar='')

        parser.add_argument('-b', '--bam',
                            action='append',
                            required=True,
                            type=str,
                            help=('Bam files for variant calling.\n'
                                  'e.g. -b bam1 -b bam2 ... \n'
                                  'You must use this option 2 times or more\n'
                                  'to get markers in following analysis.'),
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='append',
                            required=True,
                            type=str,
                            help=('Variety name of each bam file.\n'
                                  'e.g. -n name_bam1 -n name_bam2 ... \n'
                                  'You must use this option same times\n'
                                  'as -b.'),
                            metavar='')
        
        parser.add_argument('-O', '--output',
                            action='store',
                            required=True,
                            type=str,
                            help=('Identical name (must be unique).\n'
                                  'This will be stem of output directory name.'),
                            metavar='')
                            
        parser.add_argument('--cpu',
                            action='store',
                            default=2,
                            type=int,
                            help=('Number of CPUs to use.\n'),
                            metavar='')
        
        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
        
    def select_options(self):
        parser = argparse.ArgumentParser(description='chrori version {}'.format(__version__),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('chrori_select -V <VCF made by chrori_mkvcf>\n'
                        '              -O <output name>\n'
                        '              --parents <name of parental lines>\n'
                        '              --children <name of child lines>')

        # set options
        parser.add_argument('-V', '--vcf',
                            action='store',
                            required=True,
                            type=str,
                            help=('VCF file made by "chrori_mkvcf" command.\n'
                                  'VCF must contain GT and DP field.'),
                            metavar='')

        parser.add_argument('-O', '--output',
                            action='store',
                            required=True,
                            type=str,
                            help=('Identical name (must be unique).\n'
                                  'This will be stem of output directory name.'),
                            metavar='')

        parser.add_argument('-p', '--parents',
                            action='append',
                            required=True,
                            type=str,
                            help=('The names of parental lines.\n'
                                  'The names must match to VCF column names.\n'
                                  'This parameter can be specified multiple times for multiple parental lines.\n'),
                            metavar='')

        parser.add_argument('-c', '--children',
                            action='append',
                            required=True,
                            type=str,
                            help=('The names of child lines.\n'
                                  'The names must match to VCF column names.\n'
                                  'This parameter can be specified multiple times for multiple child lines.\n'),
                            metavar='')
        
        parser.add_argument('--cpu',
                            action='store',
                            default=2,
                            type=int,
                            help=('Number of CPUs to use.\n'),
                            metavar='')
        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
        
    def visual_options(self):
        parser = argparse.ArgumentParser(description='chrori version {}'.format(__version__),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('chrori_visual -i <FASTA Index file>\n'
                        '              -T <TSV which is output of chrori_select>\n'
                        '              -O <output name>\n'
                        '              --parents <name of parental lines (identical to column names of VCF)>\n'
                        '              --parents_name <name of parental lines (for visualize)>\n'
                        '              --parents_color <color of parental lines (for visualize)>\n'
                        '              --child <name of a child line (Only one line)>\n'
                        '              --genes <TSV format>\n'
                        )
        
        # set options
        parser.add_argument('-i', '--fai',
                            action='store',
                            required=True,
                            type=str,
                            help='Index file (.fai) of reference fasta.',
                            metavar='')

        parser.add_argument('-T', '--tsv',
                            action='store',
                            required=True,
                            type=str,
                            help=('TSV file which is output of chrori_select.'),
                            metavar='')
        
        parser.add_argument('-O', '--output',
                            action='store',
                            required=True,
                            type=str,
                            help=('Identical name (must be unique).\n'
                                  'This will be stem of output directory name.'),
                            metavar='')

        parser.add_argument('-p', '--parents',
                            action='append',
                            required=True,
                            type=str,
                            help=('The names of parental lines.\n'
                                  'The names must match to VCF column names.\n'
                                  'This parameter can be specified multiple times for multiple parental lines.\n'),
                            metavar='')

        parser.add_argument('--parents_name',
                            action='append',
                            default=None,
                            type=str,
                            help=('The names of parental lines for visualize.\n'
                                  'This parameter must be specified same times to --parents.\n'),
                            metavar='')

        parser.add_argument('--parents_color',
                            action='append',
                            default=None,
                            type=str,
                            help=('The colors for visualizing each parental lines.\n'
                                  'This parameter must be specified same times to --parents.\n'),
                            metavar='')

        parser.add_argument('-c', '--child',
                            action='store',
                            required=True,
                            type=str,
                            help=('The names of child line.\n'
                                  'The names must match to VCF column names.\n'
                                  'This parameter can be specified only one time.\n'),
                            metavar='')

        parser.add_argument('--genes',
                            action='store',
                            default=None,
                            type=str,
                            help=('TSV file formated for known genes information.\n'),
                            metavar='')
        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
    
    def mkvcf_check_args(self, args):
        #Does a project file with the same name exist?
        if os.path.isdir('{}_mkvcf'.format(args.output)):
            sys.stderr.write(('  Output directory already exist.\n'
                              '  Please rename the --output.\n'))
            sys.exit(1)

        if not os.path.isfile('{}'.format(args.ref)):
            sys.stderr.write('  Input reference FASTA does not exist.\n')
            sys.exit(1)

        #Do BAM files exist?
        #Is the extentions of files designeated as BAM really '.bam' ?
        for input_name in args.bam:
                if not os.path.isfile('{}'.format(input_name)):
                    sys.stderr.write('  At least one of input BAM does not exist.\n')
                    sys.exit(1)
                ext = os.path.splitext(input_name)
                if ext[-1] != '.bam':
                    sys.stderr.write(('  Please check input BAM file "{}".\n'
                                      '  The extension of this file is not "bam".\n').format(input_name))
                    sys.exit(1)

        #Do the number of BAM and the number of names match?
        if len(args.bam) != len(args.name) :
            sys.stderr.write(('  Number of input BAM files is not'
                              '  matched the number of names.\n\n'))
            sys.exit(1)

        #Names must be unique.
        name_unique = set(args.name)
        if len(args.name) != len(name_unique) :
            sys.stderr.write(('  Variety names must not be duplicated.\n\n'))
            sys.exit(1)

    def select_check_args(self, args):
        #Does a project file with the same name exist?
        if os.path.isdir('{}_select'.format(args.output)):
            sys.stderr.write(('  Output directory already exist.\n'
                              '  Please rename the --output.\n'))
            sys.exit(1)
        if not os.path.isfile('{}'.format(args.vcf)):
            sys.stderr.write('  Input VCF does not exist.\n')
            sys.exit(1)

    def visual_check_args(self, args):
        #Does a directory with the same name exist?
        if os.path.isdir('{}_visual'.format(args.output)):
            sys.stderr.write(('  Output directory already exist.\n'
                              '  Please rename the --output.\n'))
            sys.exit(1)
        if not os.path.isfile('{}'.format(args.tsv)):
            sys.stderr.write('  Input TSV does not exist.\n')
            sys.exit(1)
        if not os.path.isfile('{}'.format(args.fai)):
            sys.stderr.write('  Input FASTA index does not exist.\n')
            sys.exit(1)


