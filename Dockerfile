FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

RUN pip install coverage \
    && pip install dropbox \
    && pip install requests --upgrade \
    && ( [ $(pip show filemagic|grep -c filemagic) -eq 0 ] || pip uninstall -y filemagic ) \
    && pip install python-magic \
    && pip install mock

# Get NCBI SRATools (for fastq-dump)
RUN mkdir NCBI_SRA_tools && cd NCBI_SRA_tools && \
    curl 'https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.9.2/sratoolkit.2.9.2-ubuntu64.tar.gz' -O && \
    tar zxf sratoolkit.2.9.2-ubuntu64.tar.gz && \
    cp sratoolkit.2.9.2-ubuntu64/bin/fastq-dump.2.9.2  /kb/deployment/bin/fastq-dump

RUN pip install aiohttp==3.4.4
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
