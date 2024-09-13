# TODO - figure out how to use files as templates

TEMPLATE = """
<!--
 *  Copyright (c) 2021 GraphQL Contributors
 *  All rights reserved.
 *
 *  This source code is licensed under the license found in the
 *  LICENSE file in the root directory of this source tree.
-->
<!doctype html>
<html lang="en">
  <head>
    <title>GraphiQL</title>
    <style>
      body {
        height: 100%;
        margin: 0;
        width: 100%;
        overflow: hidden;
      }

      #graphiql {
        height: 100vh;
      }
    </style>
    <!--
      This GraphiQL example depends on Promise and fetch, which are available in
      modern browsers, but can be "polyfilled" for older browsers.
      GraphiQL itself depends on React DOM.
      If you do not want to rely on a CDN, you can host these files locally or
      include them directly in your favored resource bundler.
    -->
    <script
      src="{{ app_path_prefix }}/vendor/graphiql/react.production.min.js"
    ></script>
    <script
      src="{{ app_path_prefix }}/vendor/graphiql/react-dom.production.min.js"
    ></script>
    <!--
      These two files can be found in the npm module, however you may wish to
      copy them directly into your environment, or perhaps include them in your
      favored resource bundler.
     -->
    <script
      src="{{ app_path_prefix }}/vendor/graphiql/graphiql.min.js"
      type="application/javascript"
    ></script>
    <link rel="stylesheet" href="{{ app_path_prefix }}/vendor/graphiql/graphiql.min.css" />
    <!-- 
      These are imports for the GraphIQL Explorer plugin.
     -->
    <script
      src="{{ app_path_prefix }}/vendor/graphiql/graphiql-plugin-explorer.umd.js"
    ></script>
    <link
      rel="stylesheet"
      href="{{ app_path_prefix }}/vendor/graphiql/graphiql-plugin-explorer-style.css"
    />
  </head>

  <body>
    <div id="graphiql">Loading...</div>
    <script>
      const root = ReactDOM.createRoot(document.getElementById('graphiql'));
      const hostAndPath = `${document.location.host}${document.location.pathname}`;
      const fetcher = GraphiQL.createFetcher({
        url: `${document.location.protocol}//${hostAndPath}`,
        subscriptionUrl: `ws://${hostAndPath}`,
        headers: {
          'credentials': 'same-origin'
        },
      });
      const explorerPlugin = GraphiQLPluginExplorer.explorerPlugin();
      root.render(
        React.createElement(GraphiQL, {
          fetcher,
          defaultEditorToolsVisibility: true,
          plugins: [explorerPlugin],
        }),
      );
    </script>
  </body>
</html>"""
