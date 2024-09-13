import csv
import sys
import os

from chrori.params import Params
pm = Params('select')
args = pm.set_options()

from chrori.utils import read_vcf, time_stamp

class SelectVariants(object):
    def __init__(self, args):
        pm.select_check_args(args)
        self.args = args
        self.parents = args.parents
        self.children = args.children
        self.vcf = args.vcf

        self.stem = args.output
        self.dir = '{}_select'.format(self.stem)

    def run(self):
        print(time_stamp(),
              'Selecting variants which meet the conditions.',
              flush=True)

        #Read input VCF
        vcf_list = read_vcf(self.vcf)
        header = vcf_list[0]
        colnames = vcf_list[1]
        data = vcf_list[2]
        header.append('##selectvariants.py_{}'.format(time_stamp()))

        #Get column numbers of focused varieties.
        id_1 = [] #List of Integer
        id_2 = [] #List of Integer
        try:
            for n in self.parents:
                id_1.append(colnames.index(n))
            for n in self.children:
                id_2.append(colnames.index(n))
        except ValueError:
            print(time_stamp(), '!!ERROR!! Specified line does not exist in the VCF file\n', flush=True)
            sys.exit(1)

        #VCF format: [0]#CHROM, [1]POS, [2]ID, [3]REF, [4]ALT, [5]QUAL, [6]FILTER, [7]INFO, [8]FORMAT
        #'selected' is list of VCF rows filtered by following conditions.
        selected = []
        #'tsvrows' is list of rows output to 'self.outtsv'.
        tsvrows = []
        tsvrows_header = ['chr', 'pos', *self.parents, *self.children] #* --> expansion list

        for i in range(0,len(data)):
            if len(data[i][4].split(',')) > 1:
                continue # remove multi allelic variants

            if data[i][6] != 'PASS':
                continue # remove low quality variants

            #Check haplotype calling format.
            format = data[i][8].split(':')
            geno_1 = [] #List of haplotype calling data of parents
            geno_2 = [] #List of haplotype calling data of children

            cnt_00 = 0 #Count of '0/0' genotype in parents
            cnt_11 = 0 #Count of '1/1' genotype in parents
            name_00 = [] #Name of '0/0' genotype in parents
            name_11 = [] #Name of '1/1' genotype in parents

            parents_row = [-1] * len(self.parents)
            children_row = [-1] * len(self.children)

            for j in id_1:
                geno_1.append(data[i][j].split(':'))
            for j in id_2:
                geno_2.append(data[i][j].split(':'))
            try:
                gt_index = format.index('GT')
                c = 0 #counter
                for g in geno_1: #parent
                    if(g[gt_index] == '0/0'):
                        cnt_00 = cnt_00 + 1
                        name_00.append(self.parents[c])
                    elif(g[gt_index] == '1/1'):
                        cnt_11 = cnt_11 + 1
                        name_11.append(self.parents[c])
                    c = c + 1

                #Get unique variants for only one of parents.
                if(cnt_00 == 1 and cnt_11 == len(self.parents) - 1):
                    marker_index = self.parents.index(name_00[0])
                    marker = 0
                elif(cnt_11 == 1 and cnt_00 == len(self.parents) - 1):
                    marker_index = self.parents.index(name_11[0])
                    marker = 1
                else:
                    continue

                #modify parents_row
                c = 0 #counter
                for g in geno_1: #parents
                    if(marker == 0 and g[gt_index] == '0/0'):
                        parents_row[c] = marker_index
                    elif(marker == 1 and g[gt_index] == '1/1'):
                        parents_row[c] = marker_index

                    c = c + 1

                #modify children_row
                c = 0 #counter
                for g in geno_2: #children
                    if(marker == 0 and g[gt_index] == '0/0'):
                        children_row[c] = marker_index
                    elif(marker == 1 and g[gt_index] == '1/1'):
                        children_row[c] = marker_index
                    elif(g[gt_index] != '0/0' or g[gt_index] == '1/1'):
                        children_row[c] = -99

                    c = c + 1

            except (ValueError, IndexError):
                continue #Maybe lack of GT or DP data.

            selected.append(data[i])

            tsvrow = [data[i][0], data[i][1], *parents_row, *children_row]
            tsvrows.append(tsvrow)


        fn = '{}/{}_selected_variants.vcf'.format(self.dir, self.stem)
        with open(fn, 'w') as o:
            for h in header:
                o.write('{}\n'.format(h))
            writer = csv.writer(o, delimiter='\t')
            writer.writerow(colnames)
            writer.writerows(selected)

        fn = '{}/{}_data_for_chrori_visual.tsv'.format(self.dir, self.stem)
        with open(fn, 'w') as o:
            writer = csv.writer(o, delimiter='\t')
            writer.writerow(tsvrows_header)
            writer.writerows(tsvrows)

        print(time_stamp(),
              '{} variants are selected from {} candidates.'.format(len(selected), len(data)),
              flush=True)
        print(time_stamp(),
              'Done.',
              flush=True)

def main():
    print(time_stamp(), 'chrori_select started.', flush=True)

    prog = SelectVariants(args)
    prog.run()

    print(time_stamp(), 'chrori_select successfully finished.\n', flush=True)

if __name__ == '__main__':
    main()
