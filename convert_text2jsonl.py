import argparse, jsonlines
import numpy as np
from lxml import etree

parser = argparse.ArgumentParser(allow_abbrev=False)
# fmt: off
parser.add_argument('--ref-file', type=str, metavar='N', help='reference file name')
parser.add_argument('--ref-file-sgm', type=str, metavar='N', help='reference file name')
parser.add_argument('--sys-file', type=str, metavar='N', help='system output file')
parser.add_argument('--out-file', type=str, metavar='N', help='jsonl file name', default=None)


# TODO: sampling
args = parser.parse_args()

def output2jsonl_id(ref_file, ref_file_sgm, sys_file, out_file):
    sent_ids = []
    parser = etree.XMLParser(recover=True, encoding='utf-8')
    with open(ref_file_sgm) as fin:
        data = fin.read()
    data = etree.fromstring(data.encode('utf-8'), parser=parser)
    for doc in data:
        if 'testsuite' not in doc.keys():
            for src in doc:
                if src.tag == 'src':
                    for p in src:
                        for sent in p:
                            sent_ids.append(doc.attrib['id'] + '.' + sent.attrib['id'])
    output_lines = []
    if out_file is None:
        out_file = sys_file + '.json'
    with open(ref_file, 'rt') as fref:
        with open(sys_file, 'rt') as fsys:
            for line_ref, line_sys, sent_id in zip(fref, fsys, sent_ids):
                output_line = {}
                output_line['prediction'] = line_sys.strip()
                output_line['example_id'] = sent_id
                output_lines.append(output_line)
    #assert len(output_lines) == 2000
        
    # with jsonlines.open(out_file, 'w') as fout:
    #    fout.write_all(output_lines)
    import json
    out_dict = {} 
    for out_line in output_lines:
        out_dict[out_line['example_id']] = out_line['prediction']
    with open(out_file, 'w') as fout:
        newJson = json.dump(out_dict, fout, indent=2, separators=(',', ': '))


                
if __name__ == '__main__':
    output2jsonl_id(args.ref_file, args.ref_file_sgm, args.sys_file, args.out_file)
