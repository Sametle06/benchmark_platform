# -*- coding: utf-8 -*-
"""
Created on Mon January 3 00:03:05 2022
@author: Gokhan Ozsari
"""

from .utils import *
import warnings
import pathlib

warnings.filterwarnings('ignore')
path_to_folder = pathlib.Path(__file__).parent.resolve()
print(path_to_folder)
def usage():
    print("feature_extracter.py usage:\n")
    print("import feature_extracter:\n\n\t\t it is to import the feature extraction module\n\n")
    print("feature_extracter.extract_protein_feature(protein_feature, place_protein_id, input_folder, fasta_file_name):\n\n\
          \t This function extracts the features of the fasta file (fasta_file_name) in the input folder (input_folder)\n\
          \t by using the protein feature extraction method (protein_feature)\n\n")
    print("protein_feature: {string}, (default = 'aac_pssm'):\n\n\t\t one of the 21 PSMM-based protein descriptors in POSSUM.\n\n\
          \t ac_pssm, d_fpssm, smoothed_pssm, ab_pssm, pssm_composition, rpm_pssm,\n\
          \t s_fpssm, dpc_pssm, k_separated_bigrams_pssm, eedp, tpc, edp, rpssm,\n\
          \t pse_pssm, dp_pssm, pssm_ac, pssm_cc, aadp_pssm, aatp, medp , or all_POSSUM\n\
          \t all_POSSUM: it extracts the features of all (21) POSSUM protein descriptors\n\n\
          \t all_POSSUM: it extracts the features of all (21) POSSUM protein descriptors\n\n\
          or\n\n\
          \t one of the 18 protein descriptors in iFeature.\n\n\
          \t AAC, PAAC, APAAC, DPC, GAAC, CKSAAP, CKSAAGP, GDPC, Moran, Geary,\n\
          \t NMBroto, CTDC, CTDD, CTDT, CTriad, KSCTriad, SOCNumber, QSOrder, or all_iFeature\n\n\
          \t all_iFeature: it extracts the features of all (18) iFeature protein descriptors\n\n")
    print("place_protein_id: {int}, (default = 1):\n\n\
          \t It indicates the place of protein id in fasta header.\n\
          \t e.g. fasta header: >sp|O27002|....|....|...., seperate the header wrt. '|' then >sp is\n\
          \t in the zeroth position, protein id in the first(1) position.\n\n")
    print("input_folder: {string}, (default = 'input_folder'}:\n\n\
          \t it is the path to the folder that contains the fasta file.\n\n")
    print("fasta_file_name: {string}, (default ='sample'):\n\n\
          \t it is the name of the fasta file exclude the '.fasta' extension.\n")

class feature_extracter(object):
    '''
     The feature_extracter class is designed to extract features by employing POSSUM and iFeature python-based tools.

     POSSUM (Position-Specific Scoring matrix-based feature generator for machine learning),
     a versatile toolkit with an online web server that can generate 21 types of PSSM-based feature descriptors,
     thereby addressing a crucial need for bioinformaticians and computational biologists.

     iFeature, a versatile Python-based toolkit for generating various numerical feature representation schemes for
     both protein and peptide sequences. iFeature is capable of calculating and extracting a comprehensive spectrum
     of 18 major sequence encoding schemes that encompass 53 different types of feature descriptors.

     Parameters:
         protein_feature: {string}, (default = 'aac_pssm'): one of the 21 PSMM-based protein descriptors in POSSUM.

                          aac_pssm, d_fpssm, smoothed_pssm, ab_pssm, pssm_composition, rpm_pssm,
                          s_fpssm, dpc_pssm, k_separated_bigrams_pssm, eedp, tpc, edp, rpssm,
                          pse_pssm, dp_pssm, pssm_ac, pssm_cc, aadp_pssm, aatp, medp , or all_POSSUM

                          all_POSSUM: it extracts the features of all (21) POSSUM protein descriptors

                          or

                          one of the 18 protein descriptors in iFeature.

                          AAC, PAAC, APAAC, DPC, GAAC, CKSAAP, CKSAAGP, GDPC, Moran, Geary,
                          NMBroto, CTDC, CTDD, CTDT, CTriad, KSCTriad, SOCNumber, QSOrder, or all_iFeature

                          all_iFeature: it extracts the features of all (18) iFeature protein descriptors

         place_protein_id: {int}, (default = 1): It indicates the place of protein id in fasta header.
                           e.g. fasta header: >sp|O27002|....|....|...., seperate the header wrt. '|' then >sp is
                           in the zeroth position, protein id in the first(1) position.

        input_folder: {string}, (default = 'input_folder'}: it is the path to the folder that contains the fasta file.

        fasta_file_name: {string}, (default ='sample'): it is the name of the fasta file exclude the '.fasta' extension.
    '''

    def __init__(self, protein_feature='aac_pssm',
                 place_protein_id=1,
                 input_folder='input_folder',
                 fasta_file_name='sample'):

        self.protein_feature = protein_feature
        self.place_protein_id = place_protein_id
        self.input_folder = input_folder
        self.fasta_file_name = fasta_file_name

        self.POSSUM_desc_list = {'aac_pssm', 'd_fpssm', 'smoothed_pssm', 'ab_pssm', 'pssm_composition',
                                  'rpm_pssm', 's_fpssm', 'dpc_pssm', 'k_separated_bigrams_pssm', 'eedp',
                                  'tpc', 'edp', 'rpssm', 'pse_pssm', 'dp_pssm', 'pssm_ac', 'pssm_cc',
                                  'aadp_pssm', 'aatp', 'medp', 'tri_gram_pssm', 'all_POSSUM'}

        self.iFeature_desc_list = {'AAC', 'PAAC', 'APAAC', 'DPC', 'GAAC', 'CKSAAP', 'CKSAAGP', 'GDPC',
                                   'Moran', 'Geary', 'NMBroto', 'CTDC', 'CTDD', 'CTDT', 'CTriad',
                                   'KSCTriad', 'SOCNumber', 'QSOrder', 'all_iFeature'}

    def extract_POSSUM_feature(self):

        fasta_dict = check_form_pssm_matrices(self.input_folder, self.fasta_file_name, self.place_protein_id)

        list_desc = [self.protein_feature]

        if self.protein_feature == 'all_POSSUM':

            list_desc = self.POSSUM_desc_list - {'all_POSSUM'}

        for prot_feat in list_desc:

            temp_output_file = '{}/temp_folder/temp_output_folder/{}_{}.txt'.format(path_to_folder,
                                                                                    self.fasta_file_name,
                                                                                    prot_feat)

            os.system('python {}/POSSUM_Standalone_Toolkit/src/possum.py -i {}/{}.fasta'\
                      ' -o {} -t {} -p {}/pssm_files'.format(path_to_folder,
                                                          self.input_folder,
                                                          self.fasta_file_name,
                                                          temp_output_file,
                                                          prot_feat,
                                                          path_to_folder))

            output_file = "{}/output_folder/{}_{}.txt".format(path_to_folder,
                                                              self.fasta_file_name,
                                                              prot_feat)

            edit_extracted_features_POSSUM(temp_output_file, output_file, fasta_dict)

    def extract_iFeature_feature(self):

        list_desc = [self.protein_feature]

        if self.protein_feature == 'all_iFeature':

            list_desc = self.iFeature_desc_list - {'all_iFeature'}


        for prot_feat in list_desc:
            temp_output_file = '{}/temp_folder/temp_output_folder/{}_{}.txt'.format(path_to_folder,
                                                                                    self.fasta_file_name,
                                                                                    prot_feat)
            os.system("python {}/iFeature/iFeature.py --file {}/{}.fasta --type {}" \
                      " --out {}".format(path_to_folder,
                                         self.input_folder,
                                         self.fasta_file_name,
                                         prot_feat,
                                         temp_output_file))

            output_file = "{}/output_folder/{}_{}.txt".format(path_to_folder,
                                                              self.fasta_file_name,
                                                              prot_feat)

            edit_extracted_features_iFeature(temp_output_file, output_file, self.place_protein_id)

def extract_protein_feature(protein_feature,
                          place_protein_id,
                          input_folder,
                          fasta_file_name):

    '''
    Commmand-line dan çalıştırılma durumu için hazırlandı.

    parser = argparse.ArgumentParser(description="arguments of feature extracter module")
    parser.add_argument('--pf', type=str, default="aac_pssm", help='protein feature in POSSUM or iFeature')
    parser.add_argument('--ppid', type=str, default=1, help='the place of protein id in fasta header')
    parser.add_argument('--inpd', type=str, default="input_folder", help='path to fasta file directory')
    parser.add_argument('--fname', type=str, default="sample", help='fasta file name')

    args = parser.parse_args()

    protein_feature = args.pf
    place_protein_id = int(args.ppid)
    input_folder = args.inpd
    fasta_file_name = args.fname'''
    #input_folder = '{}/input_folder'.format(path_to_folder)
    
    feat_ext = feature_extracter(protein_feature,
                                 place_protein_id,
                                 input_folder,
                                 fasta_file_name)

    if protein_feature in feat_ext.POSSUM_desc_list:

        feat_ext.extract_POSSUM_feature()

    elif protein_feature in feat_ext.iFeature_desc_list:

        feat_ext.extract_iFeature_feature()

    else:

        print("Protein Feature extraction method is not in either POSSUM or iFeature")
