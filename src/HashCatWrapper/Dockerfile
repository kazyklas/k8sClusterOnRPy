FROM manjarolinux/base

RUN useradd -m notroot

RUN pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Sy --noconfirm base-devel git python-pip hashcat && \
    pacman -Syu --noconfirm

# Allow notroot to run stuff as root (to install dependencies):
RUN echo "notroot ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/notroot

# Continue execution (and CMD) as notroot:
USER notroot
WORKDIR /home/notroot

# install ncurses
RUN  git clone https://aur.archlinux.org/ncurses5-compat-libs.git && \
     gpg --recv-key 702353e0f7e48edb && \
     cd ncurses5-compat-libs && \
     makepkg --noconfirm --syncdeps --rmdeps --install --clean

RUN git clone https://aur.archlinux.org/intel-opencl-runtime.git && \
    cd intel-opencl-runtime && \
    makepkg --noconfirm --syncdeps --rmdeps --install --clean


RUN pip install requests 

COPY main.py /opt/main.py

COPY dict.txt /opt/dict.txt

WORKDIR /opt

CMD ["python", "main.py"]
