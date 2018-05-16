FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update
RUN pip install coverage
RUN pip install dropbox
RUN pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade \
    && ( [ $(pip show filemagic|grep -c filemagic) -eq 0 ] || pip uninstall -y filemagic ) \
    && pip install python-magic

# Get NCBI SRATools (for fastq-dump)
RUN cd /kb/dev_container/modules && \
    mkdir NCBI_SRA_tools && cd NCBI_SRA_tools && \
    curl 'https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2/sratoolkit.2.8.2-ubuntu64.tar.gz' -O && \
    tar zxf sratoolkit.2.8.2-ubuntu64.tar.gz && \
    cp sratoolkit.2.8.2-ubuntu64/bin/fastq-dump.2.8.2  /kb/deployment/bin/fastq-dump
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
