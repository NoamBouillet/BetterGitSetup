FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    clang \
    lldb \
    cmake \
    gdb \
    curl \
    git \
    python3 \
    python3-pip \
    nodejs \
    npm \
    zsh \
    bat \
    locales \
    && locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

RUN useradd -ms /bin/zsh dev && \
    su - dev -c "\
    sh -c \"\$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" --unattended"

USER dev
WORKDIR /workspace
CMD ["zsh"]
