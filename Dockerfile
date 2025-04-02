FROM ruby:3.4.2
COPY Gemfile /home/Gemfile

WORKDIR /home

RUN bundle add logger &&\
    bundler install && \
    bundle update 

RUN bundle install

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
