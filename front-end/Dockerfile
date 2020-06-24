FROM node:11.1.0-slim

# Set up NPM for `node` user and install vue-cli
ENV NPM_PACKAGES="/home/node/.npm-packages"
ENV PATH="$NPM_PACKAGES/bin:$PATH"
ENV MANPATH="$NPM_PACKAGES/share/man:$(manpath)"

RUN apt-get update && apt-get install -y git

RUN echo "prefix=$NPM_PACKAGES" >> "/home/node/.npmrc" && \
    ln -s /usr/src/app /opt/project && \
    npm install -g @vue/cli

USER node
WORKDIR /usr/src/app
#COPY ./ ./

CMD npm run serve
