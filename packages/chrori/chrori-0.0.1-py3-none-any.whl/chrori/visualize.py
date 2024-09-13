import sys
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from chrori.params import Params
pm = Params('visual')
args = pm.set_options()

from chrori.utils import read_vcf, time_stamp

class Visualize(object):
    def __init__(self, args):
        self.parents = args.parents
        self.parents_name = args.parents_name
        self.child = args.child
        self.tsv = args.tsv
        self.fai = args.fai
        self.col = args.parents_color
        self.genes = args.genes

        self.stem = args.output
        self.dir = '{}_visual'.format(self.stem)

        #Prepare chromosome information
        self.fai_data = []
        with open(self.fai, 'r') as f:
            for row in f:
                row = row.strip()
                self.fai_data.append(row.split('\t'))
        self.fai_col = ['chr', 'len', 'A', 'B', 'C']
        self.fai_data = pd.DataFrame(self.fai_data, columns=self.fai_col)
        self.fai_data['len'] = self.fai_data['len'].astype(int)

        #Read tsv file
        self.tsv_data = []
        self.tsv_col = []
        with open(self.tsv, 'r') as f:
            flag = 1
            for row in f:
                row = row.strip()
                if(flag):
                    self.tsv_col = row.split('\t')
                    flag = 0
                else:
                    self.tsv_data.append(row.split('\t'))
        self.data = pd.DataFrame(self.tsv_data, columns=self.tsv_col)
        self.data['pos'] = self.data['pos'].astype(int)
        self.data[self.parents] = self.data[self.parents].astype(int)
        self.data[self.child] = self.data[self.child].astype(int)

        #Read gene file
        self.genes_data = []
        if self.genes is not None:
            with open(self.genes, 'r') as f:
                for row in f:
                    row = row.strip()
                    self.genes_data.append(row.split('\t'))

    def mkdir(self):
        os.mkdir('{}'.format(self.dir))

    def command(self):
        #Output command info
        command = ' '.join(sys.argv)
        fn = '{}/command.txt'.format(self.dir)
        with open(fn, 'w') as f:
            f.write('{}\n'.format(command))

    def run(self):
        print(time_stamp(),
              'Drawing positions of selected markers.',
              flush=True)

        #number of digits in the length of the longest chromosome
        digits = math.floor(math.log10(max(self.fai_data['len'])))
        standard = 10**(digits)
        #if the longest chr length is 23098790,
        #digits = 7
        #standard = 10000000

        if(max(self.fai_data['len']) / standard < 2):
            standard = standard / 5
        elif(max(self.fai_data['len']) / standard < 5):
            standard = int(standard / 2)
        #if the longest chr length is 23098790,
        #standard = 5000000

        y_axis_at = range(0, standard*11, standard)
        y_axis_lab = []
        if(standard >= 100000):
            st_lab = standard/1000000
            sign = 'M'
        elif(standard >= 100):
            st_lab = standard/1000
            sign = 'K'
        else:
            st_lab = standard
            sign = 'bp'

        for i in range(11):
            y_axis_lab.append('{}{}'.format(round(st_lab * i, 1), sign))

        longest_len = max(self.fai_data['len'])




        # Create a figure
        if self.genes is None:
            fig = plt.figure(figsize=(5,5), dpi=144)
            bar_wd = 0.8
        else:
            fig = plt.figure(figsize=(10,5), dpi=144)
            bar_wd = 0.4
        ax = fig.add_subplot(111,
                             xlim=[-1, len(self.fai_data['chr'])],
                             xticks=range(len(self.fai_data['chr'])),
                             xticklabels=self.fai_data['chr'],
                             xlabel="Chromosome",
                             ylim=[longest_len*1.05, -longest_len*0.05],
                             yticks=y_axis_at,
                             yticklabels=y_axis_lab,
                             ylabel="Position")
        plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)
        plt.xticks(rotation=45)
        plt.xlim(-1, len(self.fai_data['chr']))
        plt.ylim(longest_len*1.05, -longest_len*0.05)

        legends = []
        for i in range(len(self.parents)):
            legends.append(patches.Patch(color=self.col[i], label=self.parents_name[i]))
        legends.append(patches.Patch(color='lightgray', label='Unknown'))
        ax.legend(handles=legends, loc="lower right")

        genome_len = 0 #for calculate parcentage of specific genome
        each_len = [0] * len(self.parents)
        
        for i in range(len(self.fai_data['chr'])):
            genome_len = genome_len + self.fai_data['len'][i]
            #Draw rectangle of chromosome
            r = patches.Rectangle(xy=(i-bar_wd/2, 0), width=bar_wd,
                height=self.fai_data['len'][i], ec=None, fc='lightgray', fill=True)
            ax.add_patch(r)
            
            ##make data matrix for determine the origin of genome region
            data_select = self.data[self.data['chr'] == self.fai_data['chr'][i]]
            data_select.reset_index(inplace=True, drop=True)
            mat = []

            for j in range(len(data_select)):
                num_child = data_select.loc[j, self.child]
                if(num_child >= 0):
                    mat_row = [-1] * len(self.parents)
                    mat_row[num_child] = 1
                elif(num_child == -1):
                    mat_row = [0] * len(self.parents)
                    n = max(data_select.loc[j, self.parents])
                    mat_row[n] = -1
                else: #num_child == -99
                    mat_row = [0] * len(self.parents)
                mat.append(mat_row)

            #Draw rectangle indicating origin variety
            for j in range(len(self.parents)):
                sta_0 = 0
                sta_1 = 0
                end_1 = 0
                end_0 = 0
                is_region = 0
                for k in range(len(data_select)):
                    num = mat[k][j]
                    if(num == 1):
                        if(is_region):
                            end_1 = data_select['pos'][k]
                        else:
                            is_region = 1
                            sta_1 = data_select['pos'][k]
                            end_1 = data_select['pos'][k]
                    elif(num == -1):
                        if(is_region):
                            is_region = 0
                            end_0 = data_select['pos'][k]
                            r = patches.Rectangle(xy=(i-bar_wd/2, (sta_0 + sta_1) / 2), width=bar_wd,
                                height=(end_0 + end_1) / 2 - (sta_0 + sta_1) / 2,
                                ec=None, fc=self.col[j], fill=True)
                            ax.add_patch(r)
                            each_len[j] = each_len[j] + (end_0 + end_1) / 2 - (sta_0 + sta_1) / 2
                            sta_0 = data_select['pos'][k]
                        else:
                            sta_0 = data_select['pos'][k]
                    else: #num == 0
                        pass

                if(is_region):
                    end_0 = self.fai_data['len'][i]
                    r = patches.Rectangle(xy=(i-bar_wd/2, (sta_0 + sta_1) / 2), width=bar_wd,
                        height=(end_0 + end_1) / 2 - (sta_0 + sta_1) / 2,
                        ec=None, fc=self.col[j], fill=True)
                    ax.add_patch(r)
                    each_len[j] = each_len[j] + (end_0 + end_1) / 2 - (sta_0 + sta_1) / 2
            
            #Draw rectangle of chromosome
            r = patches.Rectangle(xy=(i-bar_wd/2, 0), width=bar_wd,
                height=self.fai_data['len'][i], ec='black', fill=False)
            ax.add_patch(r)
        
        #Write known gene names
        if self.genes is not None:
            for i in range(len(self.genes_data)):
                gene_name = self.genes_data[i][0]
                chr_name = self.genes_data[i][1]
                pos = int(self.genes_data[i][2])
                chr_num = 0
                for j in range(len(self.fai_data)):
                    if(chr_name == self.fai_data['chr'][j]):
                        chr_num = j
                        break
                plt.text(chr_num - bar_wd/2, pos, gene_name, ha="right", va="top", rotation=60)
                plt.plot([chr_num - bar_wd/2, chr_num - bar_wd/(2/3)], [pos, pos], color="black", lw=1)

        # Save figure
        fn = '{}/{}_visual.png'.format(self.dir, self.stem)
        fig.savefig(fn, dpi=144)

        for j in range(len(self.parents)):
            per = each_len[j] / genome_len * 100
            print('Estimated genome region of {}: {}%'.format(self.parents[j], per))
        print(time_stamp(),
              'Done.',
              flush=True)

def main():
    print(time_stamp(), 'chrori_visual started.', flush=True)

    prog = Visualize(args)
    prog.mkdir()
    prog.command()
    prog.run()

    print(time_stamp(), 'chrori_visual successfully finished.\n', flush=True)

if __name__ == '__main__':
    main()
