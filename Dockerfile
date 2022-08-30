FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

RUN apt-get update --fix-missing
RUN apt-get install -y gcc

RUN pip install coverage==5.3.1 \
    && pip install dropbox==11.0.0 \
    && pip install requests --upgrade \
    && pip install requests_toolbelt==0.9.1 \
    && ( [ $(pip show filemagic|grep -c filemagic) -eq 0 ] || pip uninstall -y filemagic ) \
    && pip install python-magic==0.4.18 \
    && pip install mock==4.0.3 \
    && pip install aiohttp==3.4.4 \
    && pip install pyftpdlib==1.5.6

# Get NCBI SRATools (for fastq-dump)
RUN mkdir NCBI_SRA_tools && cd NCBI_SRA_tools && \
    curl 'https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.11.0/sratoolkit.2.11.0-ubuntu64.tar.gz' -O && \
    tar zxf sratoolkit.2.11.0-ubuntu64.tar.gz && \
    ln -s /NCBI_SRA_tools/sratoolkit.2.11.0-ubuntu64/bin/fastq-dump.2.11.0 /kb/deployment/bin/fastq-dump
RUN /NCBI_SRA_tools/sratoolkit.2.11.0-ubuntu64/bin/vdb-config --root --set /LIBS/GUID=1

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
