async function B() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function G(t) {
  return await B(), t().then((e) => e.default);
}
function A(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((o, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (..._) => {
        const p = _.map((a) => _ && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return e.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (c.length > 1) {
        let _ = {
          ...n.props[c[0]] || {}
        };
        o[c[0]] = _;
        for (let a = 1; a < c.length - 1; a++) {
          const h = {
            ...n.props[c[a]] || {}
          };
          _[c[a]] = h, _ = h;
        }
        const p = c[c.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, o;
      }
      const b = c[0];
      o[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function N() {
}
function H(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function J(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return N;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return J(t, (i) => e = i)(), e;
}
const w = [];
function g(t, e = N) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(u) {
    if (H(t, u) && (t = u, i)) {
      const c = !w.length;
      for (const f of n)
        f[1](), w.push(f, t);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function s(u) {
    o(u(t));
  }
  function l(u, c = N) {
    const f = [u, c];
    return n.add(f), n.size === 1 && (i = e(o, s) || N), u(t), () => {
      n.delete(f), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, Q = "$$ms-gr-antd-slots-key";
function T() {
  const t = g({});
  return O(Q, t);
}
const W = "$$ms-gr-antd-context-key";
function $(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = te(), i = ne({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), ee();
  const n = E(W), o = ((u = y(n)) == null ? void 0 : u.as_item) || t.as_item, s = n ? o ? y(n)[o] : y(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((b) => ({
      ...b,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(n)[c.as_item] : y(n);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function ee() {
  O(X, g(void 0));
}
function te() {
  return E(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function ne({
  slot: t,
  index: e,
  subIndex: i
}) {
  return O(Y, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(i)
  });
}
function je() {
  return E(Y);
}
function se(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var D = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function i() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (s = o(s, n(u)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var u in s)
        e.call(s, u) && s[u] && (l = o(l, u));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(D);
var ie = D.exports;
const M = /* @__PURE__ */ se(ie), {
  SvelteComponent: oe,
  assign: le,
  check_outros: re,
  component_subscribe: I,
  create_component: ce,
  create_slot: ae,
  destroy_component: ue,
  detach: F,
  empty: L,
  flush: d,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  get_spread_object: R,
  get_spread_update: me,
  group_outros: de,
  handle_promise: be,
  init: pe,
  insert: V,
  mount_component: he,
  noop: m,
  safe_not_equal: ge,
  transition_in: k,
  transition_out: v,
  update_await_block_branch: ye,
  update_slot_base: we
} = window.__gradio__svelte__internal;
function U(t) {
  let e, i, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ke,
    then: ve,
    catch: ke,
    value: 21,
    blocks: [, , ,]
  };
  return be(
    /*AwaitedCardMeta*/
    t[2],
    n
  ), {
    c() {
      e = L(), n.block.c();
    },
    m(o, s) {
      V(o, e, s), n.block.m(o, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, i = !0;
    },
    p(o, s) {
      t = o, ye(n, t, s);
    },
    i(o) {
      i || (k(n.block), i = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        v(l);
      }
      i = !1;
    },
    d(o) {
      o && F(e), n.block.d(o), n.token = null, n = null;
    }
  };
}
function ke(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function ve(t) {
  let e, i;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: M(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-card-meta"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    {
      avatar: (
        /*$mergedProps*/
        t[0].avatar
      )
    },
    {
      description: (
        /*$mergedProps*/
        t[0].description
      )
    },
    {
      title: (
        /*$mergedProps*/
        t[0].title
      )
    },
    /*$mergedProps*/
    t[0].props,
    A(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Ce]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    o = le(o, n[s]);
  return e = new /*CardMeta*/
  t[21]({
    props: o
  }), {
    c() {
      ce(e.$$.fragment);
    },
    m(s, l) {
      he(e, s, l), i = !0;
    },
    p(s, l) {
      const u = l & /*$mergedProps, $slots*/
      3 ? me(n, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: M(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-card-meta"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && {
        avatar: (
          /*$mergedProps*/
          s[0].avatar
        )
      }, l & /*$mergedProps*/
      1 && {
        description: (
          /*$mergedProps*/
          s[0].description
        )
      }, l & /*$mergedProps*/
      1 && {
        title: (
          /*$mergedProps*/
          s[0].title
        )
      }, l & /*$mergedProps*/
      1 && R(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && R(A(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }]) : {};
      l & /*$$scope*/
      524288 && (u.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(u);
    },
    i(s) {
      i || (k(e.$$.fragment, s), i = !0);
    },
    o(s) {
      v(e.$$.fragment, s), i = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function Ce(t) {
  let e;
  const i = (
    /*#slots*/
    t[18].default
  ), n = ae(
    i,
    t,
    /*$$scope*/
    t[19],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, s) {
      n && n.m(o, s), e = !0;
    },
    p(o, s) {
      n && n.p && (!e || s & /*$$scope*/
      524288) && we(
        n,
        i,
        o,
        /*$$scope*/
        o[19],
        e ? _e(
          i,
          /*$$scope*/
          o[19],
          s,
          null
        ) : fe(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      e || (k(n, o), e = !0);
    },
    o(o) {
      v(n, o), e = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function Ke(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Se(t) {
  let e, i, n = (
    /*$mergedProps*/
    t[0].visible && U(t)
  );
  return {
    c() {
      n && n.c(), e = L();
    },
    m(o, s) {
      n && n.m(o, s), V(o, e, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && k(n, 1)) : (n = U(o), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (de(), v(n, 1, 1, () => {
        n = null;
      }), re());
    },
    i(o) {
      i || (k(n), i = !0);
    },
    o(o) {
      v(n), i = !1;
    },
    d(o) {
      o && F(e), n && n.d(o);
    }
  };
}
function Pe(t, e, i) {
  let n, o, s, {
    $$slots: l = {},
    $$scope: u
  } = e;
  const c = G(() => import("./card.meta-4Y206Ndz.js"));
  let {
    gradio: f
  } = e, {
    _internal: b = {}
  } = e, {
    avatar: _
  } = e, {
    description: p
  } = e, {
    title: a
  } = e, {
    as_item: h
  } = e, {
    props: C = {}
  } = e;
  const z = g(C);
  I(t, z, (r) => i(17, n = r));
  let {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: P = {}
  } = e, {
    visible: j = !0
  } = e;
  const q = T();
  I(t, q, (r) => i(1, s = r));
  const [x, Z] = $({
    gradio: f,
    props: n,
    _internal: b,
    as_item: h,
    visible: j,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    avatar: _,
    description: p,
    title: a
  });
  return I(t, x, (r) => i(0, o = r)), t.$$set = (r) => {
    "gradio" in r && i(6, f = r.gradio), "_internal" in r && i(7, b = r._internal), "avatar" in r && i(8, _ = r.avatar), "description" in r && i(9, p = r.description), "title" in r && i(10, a = r.title), "as_item" in r && i(11, h = r.as_item), "props" in r && i(12, C = r.props), "elem_id" in r && i(13, K = r.elem_id), "elem_classes" in r && i(14, S = r.elem_classes), "elem_style" in r && i(15, P = r.elem_style), "visible" in r && i(16, j = r.visible), "$$scope" in r && i(19, u = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    4096 && z.update((r) => ({
      ...r,
      ...C
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, as_item, visible, elem_id, elem_classes, elem_style, avatar, description, title*/
    257984 && Z({
      gradio: f,
      props: n,
      _internal: b,
      as_item: h,
      visible: j,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      avatar: _,
      description: p,
      title: a
    });
  }, [o, s, c, z, q, x, f, b, _, p, a, h, C, K, S, P, j, n, l, u];
}
class Ne extends oe {
  constructor(e) {
    super(), pe(this, e, Pe, Se, ge, {
      gradio: 6,
      _internal: 7,
      avatar: 8,
      description: 9,
      title: 10,
      as_item: 11,
      props: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15,
      visible: 16
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), d();
  }
  get avatar() {
    return this.$$.ctx[8];
  }
  set avatar(e) {
    this.$$set({
      avatar: e
    }), d();
  }
  get description() {
    return this.$$.ctx[9];
  }
  set description(e) {
    this.$$set({
      description: e
    }), d();
  }
  get title() {
    return this.$$.ctx[10];
  }
  set title(e) {
    this.$$set({
      title: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
}
export {
  Ne as I,
  je as g,
  g as w
};
