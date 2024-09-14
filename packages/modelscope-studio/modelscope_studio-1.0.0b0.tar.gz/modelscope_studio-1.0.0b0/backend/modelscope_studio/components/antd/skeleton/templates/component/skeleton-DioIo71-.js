import { g as U, w as f } from "./Index-BjwKfcKp.js";
const k = window.ms_globals.ReactDOM.createPortal, W = window.ms_globals.antd.Skeleton, {
  SvelteComponent: j,
  assign: v,
  binding_callbacks: y,
  check_outros: A,
  component_subscribe: S,
  compute_slots: B,
  create_slot: F,
  detach: d,
  element: K,
  empty: G,
  exclude_internal_props: h,
  get_all_dirty_from_scope: H,
  get_slot_changes: J,
  group_outros: L,
  init: Q,
  insert: m,
  safe_not_equal: T,
  set_custom_element_data: x,
  space: V,
  transition_in: p,
  transition_out: b,
  update_slot_base: X
} = window.__gradio__svelte__internal, {
  beforeUpdate: Y,
  getContext: Z,
  onDestroy: $,
  setContext: ee
} = window.__gradio__svelte__internal;
function C(l) {
  let t, o;
  const a = (
    /*#slots*/
    l[7].default
  ), s = F(
    a,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), s && s.c(), x(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      m(e, t, n), s && s.m(t, null), l[9](t), o = !0;
    },
    p(e, n) {
      s && s.p && (!o || n & /*$$scope*/
      64) && X(
        s,
        a,
        e,
        /*$$scope*/
        e[6],
        o ? J(
          a,
          /*$$scope*/
          e[6],
          n,
          null
        ) : H(
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
      b(s, e), o = !1;
    },
    d(e) {
      e && d(t), s && s.d(e), l[9](null);
    }
  };
}
function te(l) {
  let t, o, a, s, e = (
    /*$$slots*/
    l[4].default && C(l)
  );
  return {
    c() {
      t = K("react-portal-target"), o = V(), e && e.c(), a = G(), x(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      m(n, t, c), l[8](t), m(n, o, c), e && e.m(n, c), m(n, a, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = C(n), e.c(), p(e, 1), e.m(a.parentNode, a)) : e && (L(), b(e, 1, 1, () => {
        e = null;
      }), A());
    },
    i(n) {
      s || (p(e), s = !0);
    },
    o(n) {
      b(e), s = !1;
    },
    d(n) {
      n && (d(t), d(o), d(a)), l[8](null), e && e.d(n);
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
function se(l, t, o) {
  let a, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = B(e);
  let {
    svelteInit: i
  } = t;
  const w = f(P(t)), u = f();
  S(l, u, (r) => o(0, a = r));
  const _ = f();
  S(l, _, (r) => o(1, s = r));
  const I = [], R = Z("$$ms-gr-antd-react-wrapper"), {
    slotKey: q,
    slotIndex: z,
    subSlotIndex: E
  } = U() || {}, M = i({
    parent: R,
    props: w,
    target: u,
    slot: _,
    slotKey: q,
    slotIndex: z,
    subSlotIndex: E,
    onDestroy(r) {
      I.push(r);
    }
  });
  ee("$$ms-gr-antd-react-wrapper", M), Y(() => {
    w.set(P(t));
  }), $(() => {
    I.forEach((r) => r());
  });
  function N(r) {
    y[r ? "unshift" : "push"](() => {
      a = r, u.set(a);
    });
  }
  function O(r) {
    y[r ? "unshift" : "push"](() => {
      s = r, _.set(s);
    });
  }
  return l.$$set = (r) => {
    o(17, t = v(v({}, t), h(r))), "svelteInit" in r && o(5, i = r.svelteInit), "$$scope" in r && o(6, n = r.$$scope);
  }, t = h(t), [a, s, u, _, c, i, n, e, N, O];
}
class ne extends j {
  constructor(t) {
    super(), Q(this, t, se, te, T, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, g = window.ms_globals.tree;
function oe(l) {
  function t(o) {
    const a = f(), s = new ne({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: a,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? g;
          return c.nodes = [...c.nodes, n], D({
            createPortal: k,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== a), D({
              createPortal: k,
              node: g
            });
          }), n;
        },
        ...o.props
      }
    });
    return a.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const re = oe(W);
export {
  re as Skeleton,
  re as default
};
