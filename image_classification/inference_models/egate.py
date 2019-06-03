import os
import csv
import sys
import glob
import json
import time
import psutil
import argparse
from . import predict as PR
from pprint import pprint
from bxingest.models.common import ImageDescriptor


class Egate(object):
    def __init__(self, model_dir):
        self.model_dir = model_dir
        model_file = "{}/retrained_graph.pb".format(model_dir)
        label_file = "{}/retrained_labels.txt".format(model_dir)
        self.graph = PR.load_graph(model_file)
        self.labels = PR.load_labels(label_file)

    def is_egate(self, image_descriptors):
        """
        Return a dict of true/false corresponding to each image in the list.

        Input:
        - image_filenames with full path
        Output
        - Binary classification. True => egate, False => not an egate
        """
        desc_dict = dict(image_descriptors)
        results, _ = PR.process_images(desc_dict.keys(),
                                       graph=self.graph,
                                       output_operation=PR.output_operation(
                                           self.graph, PR.output_name),
                                       input_operation=PR.input_operation(
                                           self.graph, PR.input_name),
                                        input_height=PR.input_height,
                                        input_width=PR.input_width,
                                        input_mean=PR.input_mean,
                                        input_std=PR.input_std)
        summary = {}
        for im, res in results:
            top_k = res.argsort()[-5:][::-1]
            res_dict = dict(([("image", im)] +
                             [(self.labels[i], 100*res[i]) for i in top_k]))
            summary[im] = res_dict["airport"] < 50.0
        summary = {desc_dict[im]:v for im, v in summary.items()}
        return summary

    def is_egate2(self, image_descriptors):
        """
        Return a dict of true/false corresponding to each image in the list.

        Input:
        - image_filenames with full path
        Output
        - Binary classification. True => egate, False => not an egate
        """
        desc_dict = dict(image_descriptors)
        results, fails = PR.process_images(desc_dict.keys(),
                                           graph=self.graph,
                                            output_operation=PR.output_operation(
                                                self.graph, PR.output_name),
                                            input_operation=PR.input_operation(
                                                self.graph, PR.input_name),
                                            input_height=PR.input_height,
                                            input_width=PR.input_width,
                                            input_mean=PR.input_mean,
                                            input_std=PR.input_std)
        summary = {}
        for im, res in results:
            top_k = res.argsort()[::-1]
            # res_dict = dict(([("image", im)] +
            #                  [(self.labels[i], 100*res[i]) for i in top_k]))
            # print("{} => {}".format(im, res_dict))
            # summary[im] = "egates" in res_dict.keys()
            summary[im] = [(self.labels[i], 100*res[i]) for i in top_k]
        summary = {desc_dict[im]:v for im, v in summary.items()}
        return summary, fails


def batch_images(images, batch_size):
    index = 0
    while index < len(images):
        yield images[index : index+batch_size]
        index += batch_size


def main(args):
    print(args)
    csv_res = args.csv_filename
    csv_prof = args.profile_csv
    details_file = args.detailed_results_json
    detailed_data = {}
    if args.wild_images_dir and args.model_dir:
        count = args.max_to_process
        images = glob.glob("{}/**/*.jpg".format(args.wild_images_dir),
                           recursive=True)
        if count > 0:
            images = images[:count]
        if not images:
            print("No jpg images found in {}".format(args.wild_images_dir))
            return

        images = [ImageDescriptor(im, args.csv_results_key + im) for im in images]
        eg = Egate(model_dir=args.model_dir)
        fn_is_egate = eg.is_egate if args.use_old_training else eg.is_egate2
        how_many_egates = 0
        if csv_res:
            print("Found {} jpg images to process".format(len(images)))
            with open(csv_res, "w") as f, open(csv_prof, "w") as pf:
                pfw = csv.writer(pf)
                pfw.writerow(["batch_index","t_delta", "memory", "mem-delta"])
                f.write("image,is_egate\n")
                m_last = 0
                img_processed = 0
                failed_images = []
                for i, batch in enumerate(
                        batch_images(images, batch_size=args.batch_size)):
                    start = time.time()
                    if args.use_old_training:
                        summary = fn_is_egate(batch)
                        for k_, v_ in summary.items():
                            how_many_egates += 1 if v_ else 0
                    else:
                        summary, fails_ = fn_is_egate(batch)
                        if fails_:
                            failed_images.extend(fails_)
                        summary2 = {}
                        for k,v in summary.items():
                            summary2[k] = v[0][0] == args.egates_tagname
                            how_many_egates += 1 if summary2[k] else 0
                            details_as_dict = {}
                            for tag_, conf_ in v:
                                details_as_dict[tag_] = "{:.1f}".format(conf_)
                            detailed_data[k] = details_as_dict
                        summary = summary2
                    end = time.time()
                    cw = csv.writer(f)
                    for k,v in summary.items():
                        cw.writerow([k,v])
                        img_processed += 1
                    memory = psutil.Process(os.getpid()).memory_info().rss
                    pfw.writerow([i, "{:.2f}".format(end - start),
                                  memory, memory-m_last])
                    m_last = memory
                    f.flush()
                    pf.flush()
            with open(details_file, "w") as f:
                f.write(json.dumps(detailed_data, indent=2))
            if failed_images:
                pprint(failed_images)
                print("{} images failed".format(len(failed_images)))
            print("Processed {} images (success: {}) , predicted {} egates".format(
                len(images), img_processed, how_many_egates))
        else:
            summary = fn_is_egate(images[:count])
            pprint({os.path.split(k)[-1]:v for k,v in summary.items()})
    else:
        print("Use it as a library, for is_egate() API")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test in progress')
    parser.add_argument('--model-dir')
    parser.add_argument('--csv-filename', help="csv for imagename, true/false")
    parser.add_argument('--wild-images-dir')
    parser.add_argument('--profile-csv', default='profile.csv')
    parser.add_argument('--batch-size', default=100, type=int)
    parser.add_argument('--max-to-process', default=0, type=int)
    parser.add_argument('--use-old-training', action='store_true')
    parser.add_argument('--csv-results-key', default="key_")
    parser.add_argument('--egates-tagname', default="egates")
    parser.add_argument('--detailed-results-json', default="csv-detailed.json")
    main(parser.parse_args())
