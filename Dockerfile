FROM ruby:3.4.2-alpine

WORKDIR /home

COPY Gemfile ./

RUN apk add --no-cache build-base && \
    gem install jekyll bundler && \
    bundle install --jobs=4 --retry=3 && \
    apk del build-base

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
