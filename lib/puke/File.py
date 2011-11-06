import os, os.path, shutil, logging, sys

YUI_COMPRESSOR = sys.argv[0] + 'compress'


def compress(in_files, out_file, in_type='js', verbose=False,
             temp_file='.temp'):
    
    temp = open(temp_file, 'w')
    for f in in_files:
        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        temp.write(data)

        logging.info(' + %s' % f)
    temp.close()

    options = ['-o "%s"' % out_file,
               '--type %s' % in_type]

    if verbose:
        options.append('-v')
    logging.info(os.system('pwd'))
    os.system('java -jar "%s" %s "%s"' % (YUI_COMPRESSOR,
                                          ' '.join(options),
                                          temp_file))

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    logging.info('=> %s' % out_file)
    logging.info('Original: %.2f kB' % (org_size / 1024.0))
    logging.info('Compressed: %.2f kB' % (new_size / 1024.0))
    logging.info('Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100))
    logging.info('')

    #os.remove(temp_file)