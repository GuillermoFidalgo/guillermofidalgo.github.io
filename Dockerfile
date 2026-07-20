FROM ruby:3.4.2-slim-bookworm

WORKDIR /srv/jekyll

COPY Gemfile /srv/jekyll

RUN apt-get update && apt-get install -y build-essential  && \
    gem install jekyll bundler && \
    bundle install --jobs=4 --retry=3 
    # && \ 
    # apt-get autoremove -y && apt-get clean

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0","--force_polling"]
