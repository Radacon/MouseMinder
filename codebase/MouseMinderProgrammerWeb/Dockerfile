FROM node:22-alpine

WORKDIR /app
COPY package.json server.mjs ./
COPY public ./public
COPY firmware ./firmware
COPY data ./data

RUN chown -R node:node /app
USER node

ENV HOST=0.0.0.0
ENV PORT=8787
EXPOSE 8787
VOLUME ["/app/data"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:8787/api/health').then(r=>{if(!r.ok)process.exit(1)}).catch(()=>process.exit(1))"

CMD ["node", "server.mjs"]
