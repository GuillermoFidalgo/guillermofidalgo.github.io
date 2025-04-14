FROM ruby:3.4.2
COPY Gemfile /home/Gemfile

WORKDIR /home

RUN bundle add logger &&\
    bundler install && \
    gem install dnsruby csv logger faraday faraday-retry && \
    bundle update 

RUN bundler install

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
