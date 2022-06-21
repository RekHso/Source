FROM rekhso/source:slim-buster

#clonning repo 
RUN git clone https://github.com/rekhso/source.git /root/hsorek
#working directory 
WORKDIR /root/hsorek

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/hsorek/bin:$PATH"

CMD ["python3","-m","hsorek"]
