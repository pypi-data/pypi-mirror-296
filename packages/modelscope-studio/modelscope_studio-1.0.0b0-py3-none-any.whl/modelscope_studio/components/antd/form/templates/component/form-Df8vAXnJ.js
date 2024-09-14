import { g as B, w as f } from "./Index-DguM8lXH.js";
const z = window.ms_globals.React, A = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, k = window.ms_globals.antd.Form;
var F = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J = z, M = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), G = Object.prototype.hasOwnProperty, H = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(l, t, o) {
  var n, s = {}, e = null, r = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (n in t) G.call(t, n) && !Q.hasOwnProperty(n) && (s[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) s[n] === void 0 && (s[n] = t[n]);
  return {
    $$typeof: M,
    type: l,
    key: e,
    ref: r,
    props: s,
    _owner: H.current
  };
}
b.Fragment = Y;
b.jsx = j;
b.jsxs = j;
F.exports = b;
var X = F.exports;
const {
  SvelteComponent: Z,
  assign: x,
  binding_callbacks: R,
  check_outros: V,
  component_subscribe: S,
  compute_slots: $,
  create_slot: ee,
  detach: d,
  element: D,
  empty: te,
  exclude_internal_props: E,
  get_all_dirty_from_scope: se,
  get_slot_changes: oe,
  group_outros: ne,
  init: re,
  insert: m,
  safe_not_equal: le,
  set_custom_element_data: C,
  space: ie,
  transition_in: p,
  transition_out: g,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: ae,
  getContext: _e,
  onDestroy: ue,
  setContext: fe
} = window.__gradio__svelte__internal;
function O(l) {
  let t, o;
  const n = (
    /*#slots*/
    l[7].default
  ), s = ee(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), s && s.c(), C(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      m(e, t, r), s && s.m(t, null), l[9](t), o = !0;
    },
    p(e, r) {
      s && s.p && (!o || r & /*$$scope*/
      64) && ce(
        s,
        n,
        e,
        /*$$scope*/
        e[6],
        o ? oe(
          n,
          /*$$scope*/
          e[6],
          r,
          null
        ) : se(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (p(s, e), o = !0);
    },
    o(e) {
      g(s, e), o = !1;
    },
    d(e) {
      e && d(t), s && s.d(e), l[9](null);
    }
  };
}
function de(l) {
  let t, o, n, s, e = (
    /*$$slots*/
    l[4].default && O(l)
  );
  return {
    c() {
      t = D("react-portal-target"), o = ie(), e && e.c(), n = te(), C(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      m(r, t, c), l[8](t), m(r, o, c), e && e.m(r, c), m(r, n, c), s = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = O(r), e.c(), p(e, 1), e.m(n.parentNode, n)) : e && (ne(), g(e, 1, 1, () => {
        e = null;
      }), V());
    },
    i(r) {
      s || (p(e), s = !0);
    },
    o(r) {
      g(e), s = !1;
    },
    d(r) {
      r && (d(t), d(o), d(n)), l[8](null), e && e.d(r);
    }
  };
}
function P(l) {
  const {
    svelteInit: t,
    ...o
  } = l;
  return o;
}
function me(l, t, o) {
  let n, s, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const c = $(e);
  let {
    svelteInit: a
  } = t;
  const y = f(P(t)), _ = f();
  S(l, _, (i) => o(0, n = i));
  const u = f();
  S(l, u, (i) => o(1, s = i));
  const v = [], N = _e("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L
  } = B() || {}, T = a({
    parent: N,
    props: y,
    target: _,
    slot: u,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: L,
    onDestroy(i) {
      v.push(i);
    }
  });
  fe("$$ms-gr-antd-react-wrapper", T), ae(() => {
    y.set(P(t));
  }), ue(() => {
    v.forEach((i) => i());
  });
  function U(i) {
    R[i ? "unshift" : "push"](() => {
      n = i, _.set(n);
    });
  }
  function W(i) {
    R[i ? "unshift" : "push"](() => {
      s = i, u.set(s);
    });
  }
  return l.$$set = (i) => {
    o(17, t = x(x({}, t), E(i))), "svelteInit" in i && o(5, a = i.svelteInit), "$$scope" in i && o(6, r = i.$$scope);
  }, t = E(t), [n, s, _, u, c, a, r, e, U, W];
}
class pe extends Z {
  constructor(t) {
    super(), re(this, t, me, de, le, {
      svelteInit: 5
    });
  }
}
const h = window.ms_globals.rerender, w = window.ms_globals.tree;
function be(l) {
  function t(o) {
    const n = f(), s = new pe({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, r], h({
            createPortal: I,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== n), h({
              createPortal: I,
              node: w
            });
          }), r;
        },
        ...o.props
      }
    });
    return n.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const ge = be(({
  value: l,
  onValueChange: t,
  onValuesChange: o,
  ...n
}) => {
  const [s] = k.useForm();
  return A(() => {
    s.setFieldsValue(l);
  }, [s, l]), /* @__PURE__ */ X.jsx(k, {
    ...n,
    initialValues: l,
    form: s,
    onValuesChange: (e, r) => {
      t(r), o == null || o(e, r);
    }
  });
});
export {
  ge as Form,
  ge as default
};
